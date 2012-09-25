############
安装
############

本文假定你熟悉Python和Django，包括了一些主要步骤，完成后可以参看 :doc:`tutorial`。

************
要求
************

* `Python`_ 2.5 (或更高的2.x版本).
* `Django`_ 1.3.1或1.4.
* `South`_ 0.7.2或更高
* `PIL`_ 1.1.6或更高
* `django-classy-tags`_ 0.3.4.1或更高
* `django-mptt`_ 0.5.2 (因为兼容性的原因，必须使用这个版本)
* `django-sekizai`_ 0.6.1或更高
* `html5lib`_ 0.90或更高
* `Databases`_ 一节中列出的一种数据库。

.. 注意:: 如使用pip安装django CMS，Django, django-mptt, django-classy-tags, 
          django-sekizai, south和html5lib会自动安装。

.. _Python: http://www.python.org
.. _Django: http://www.djangoproject.com
.. _PIL: http://www.pythonware.com/products/pil/
.. _South: http://south.aeracode.org/
.. _django-classy-tags: https://github.com/ojii/django-classy-tags
.. _django-mptt: https://github.com/django-mptt/django-mptt
.. _django-sekizai: https://github.com/ojii/django-sekizai
.. _html5lib: http://code.google.com/p/html5lib/

推荐
===========

* 用 `django-filer`_ 及 `django CMS plugins`_, 一个文件、图像管理应用，替代某些核心插件
* `django-reversion`_ 1.6, 为你的内容提供版本支持

.. _django-filer: https://github.com/stefanfoulis/django-filer
.. _django CMS plugins: https://github.com/stefanfoulis/cmsplugin-filer
.. _django-reversion: https://github.com/etianen/django-reversion

在Ubuntu上安装
==============

.. 警告::

    下面的指令会在全局安装某些软件包，如PIL, Django, South和django CMS，不建议这    么做。我们建议使用 `virtualenv`_ ，这样就会把Django, django CMS和South安装在    一个python的虚拟环境里。

如果你用的是Ubuntu (在10.10上测试过)，可以用下面的步骤：

.. code-block:: bash

    sudo aptitude install python2.6 python-setuptools python-imaging
    sudo easy_install pip
    sudo pip install Django==1.4 django-cms south

另外，你需要所选数据库的Python驱动程序:

.. code-block:: bash

    sudo aptitude python-psycopg2

或

.. code-block:: bash

    sudo aptitude install python-mysql

上述命令会在全局安装PIL和数据库的驱动程序。

现在你已完成了初步安装，下一步可以参看 :doc:`tutorial`。


On Mac OSX
==========

**TODO** (Should setup everything up to but not including
"pip install django-cms" like the above)

On Microsoft Windows
====================

**TODO**.

*********
数据库
*********

我们建议使用 `PostgreSQL`_ 或 `MySQL`_ 作为django CMS的数据库。数据库系统的安装、使用，不属于本文档的范围，在这些软件的网站上有很好的文档。

为了有效地使用django CMS，我们建议：

* 为django CMS使用一套单独的credentials；
* 为django CMS创建一个独立的数据库。

.. _PostgreSQL: http://www.postgresql.org/
.. _MySQL: http://www.mysql.com
.. _virtualenv: http://www.virtualenv.org/
