from django import template
from django.core.cache import cache
from django.utils.safestring import SafeUnicode

from cms import settings
from cms.models import Content, Page, Title
from cms.utils import get_language_from_request, get_page_from_request

register = template.Library()

def get_page_children_for_site(page, site):
    if page:
        return page.get_children().filter(sites__domain=site.domain)
    else:
        return []
    
def find_children(target, pages):
    if not hasattr(target, "childrens"):
        target.childrens = []
    for page in pages:
        if page.parent_id and page.parent_id == target.pk:
            if hasattr(target, "selected") or hasattr(target, "descendant"):
                page.descendant = True
            target.childrens.append(page)
            #pages.remove(page)
            find_children(page, pages)
    

def show_menu(context, from_level=0, to_level=100, render_children=False, next_page=None):
    """
    render a nested list of all children of the pages
    from_level: is the start level
    to_level: is the max level rendered
    render_children: if set to True will render all not direct ascendants too
    """
    request = context['request']
    site = request.site
    CMS_CONTENT_CACHE_DURATION = settings.CMS_CONTENT_CACHE_DURATION
    lang = get_language_from_request(request)
    if 'current_page' in context:
        current_page = get_page_from_request(context)# TODO: change to request
    if not next_page: #new menu... get all the data so we can save a lot of queries
        ids = []
        children = []
        ancestors = current_page.get_ancestors().values_list('id', flat=True)
        pages = list(Page.objects.published())#.filter(level__gte=from_level, level__lte=to_level))
        all_pages = pages[:]
        for page in pages:
            ids.append(page.pk)
            if page.pk == current_page.pk:
                page.selected = True
            if page.level == from_level:
                children.append(page)
                #pages.remove(page)
                find_children(page, pages)
        titles = Title.objects.filter(pk__in=ids, language=lang)
        for page in all_pages:
            for title in titles:
                if title.page_id == page.pk:
                    page.title_cache = title
            
            if page.pk in ancestors:
                page.ancestor = True
            if page.parent_id == current_page.parent_id and not page.pk == current_page.pk:
                page.sibling = True
            
    else:
        if next_page.childrens:
            children = next_page.childrens
        else:
            children = []
    return locals()
show_menu = register.inclusion_tag('cms/menu.html', takes_context=True)(show_menu)

def show_sub_menu(context, page, url='/'):
    """Get the root page of the current page and 
    render a nested list of all root's children pages"""
    root = page.get_root()
    request = context['request']
    site = request.site
    children = get_page_children_for_site(page, site)
    if 'current_page' in context:
        current_page = context['current_page']
    return locals()
show_sub_menu = register.inclusion_tag('cms/sub_menu.html',
                                       takes_context=True)(show_sub_menu)

def show_admin_menu(context, page, url='/admin/cms/page/', level=None):
    """Render the admin table of pages"""
    request = context['request']
    site = request.site
    children = get_page_children_for_site(page, site)
    has_permission = page.has_page_permission(request)
    # level is used to add a left margin on table row
    if has_permission:
        if level is None:
            level = 0
        else:
            level = level+3
    return locals()
show_admin_menu = register.inclusion_tag('admin/cms/page/menu.html',
                                         takes_context=True)(show_admin_menu)

def has_permission(page, request):
    return page.has_page_permission(request)
register.filter(has_permission)

def show_content(context, content_type, lang=None):
    """Display a content type from a page.
    
    eg: {% show_content page_object "title" %}
    
    You can also use the slug of a page
    
    eg: {% show_content "my-page-slug" "title" %}
    
    Keyword arguments:
    page -- the page object
    args -- content_type used by a placeholder
    lang -- the wanted language (default None, use the request object to know)
    """
    page = get_page_from_request(context)
    request = context.get('request', False)
    if not request or not page:
        return {'content':''}
    # if the page is a SafeUnicode, try to use it like a slug
    if isinstance(page, SafeUnicode):
        c = Content.objects.filter(type='slug', body=page)
        if len(c):
            page = c[0].page
        else:
            return {'content':''}
    if lang is None:
        lang = get_language_from_request(context['request'])
    if hasattr(settings, 'CMS_CONTENT_CACHE_DURATION'):
        key = 'content_cache_pid:'+str(page.id)+'_l:'+str(lang)+'_type:'+str(content_type)
        c = cache.get(key)
        if not c:
            c = Content.objects.get_content(page, lang, content_type, True)
            cache.set(key, c, settings.CMS_CONTENT_CACHE_DURATION)
    else:
        c = Content.objects.get_content(page, lang, content_type, True)
    if c:
        return {'content':c}
    return {'content':''}
show_content = register.inclusion_tag('cms/content.html',
                                      takes_context=True)(show_content)

def show_absolute_url(context, page, lang=None):
    """Show the url of a page in the right language"""
    request = context.get('request', False)
    if not request or not page:
        return {'content':''}
    if lang is None:
        lang = get_language_from_request(context['request'])
    if hasattr(settings, 'CMS_CONTENT_CACHE_DURATION'):
        key = 'page_url_pid:'+str(page.id)+'_l:'+str(lang)+'_type:absolute_url'
        url = cache.get(key)
        if not url:
            url = page.get_absolute_url(language=lang)
            cache.set(key, url, settings.CMS_CONTENT_CACHE_DURATION)
    else:
        url = page.get_absolute_url(language=lang)
    if url:
        return {'content':url}
    return {'content':''}
show_absolute_url = register.inclusion_tag('cms/content.html',
                                      takes_context=True)(show_absolute_url)

def show_revisions(context, page, content_type, lang=None):
    """Render the last 10 revisions of a page content with a list"""
    if not settings.CMS_CONTENT_REVISION:
        return {'revisions':None}
    revisions = Content.objects.filter(page=page, language=lang,
                                type=content_type).order_by('-creation_date')
    if len(revisions) < 2:
        return {'revisions':None}
    return {'revisions':revisions[0:10]}

show_revisions = register.inclusion_tag('cms/revisions.html',
                                        takes_context=True)(show_revisions)

def do_placeholder(parser, token):
    error_string = '%r tag requires three arguments' % token.contents[0]
    try:
        # split_contents() knows not to split quoted strings.
        bits = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(error_string)
    if len(bits) == 2:
        #tag_name, name
        return PlaceholderNode(bits[1])
    elif len(bits) == 3:
        #tag_name, name, widget
        return PlaceholderNode(bits[1], bits[2])
    else:
        raise template.TemplateSyntaxError(error_string)

class PlaceholderNode(template.Node):
    """This template node is used to output page content and
    is also used in the admin to dynamicaly generate input fields.
    
    eg: {% placeholder content-type-name page-object widget-name %}
    
    Keyword arguments:
    content-type-name -- the content type you want to show/create
    page-object -- the page object
    widget-name -- the widget name you want into the admin interface. Take
        a look into pages.admin.widgets to see which widgets are available.
    """
    def __init__(self, name, widget=None):
        self.name = name
        self.widget = widget

    def render(self, context):
        self.page = get_page_from_request(context) #TODO: change to request
        if not 'request' in context:
            return ''
        l = get_language_from_request(context['request'])
        request = context['request']
        if self.name.lower() == "title":
            c = Title.objects.get_title(self.page, l).title
        elif self.name.lower() == "slug":
            c = Title.objects.get_title(self.page, l).slug
        else:
            c = Content.objects.get_content(self.page, l, self.name, True)
        if not c:
            return ''
        return '<div id="%s" class="placeholder">%s</div>' % (self.name, c)
        
    def __repr__(self):
        return "<Placeholder Node: %s>" % self.name

register.tag('placeholder', do_placeholder)