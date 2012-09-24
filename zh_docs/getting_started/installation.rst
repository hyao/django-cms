############
安装
############

本文假定你熟悉Python和Django。
It should
outline the steps necessary for you to follow the :doc:`tutorial`.

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

建议
===========

* 用 `django-filer`_ 及 `django CMS plugins`_, 一个文件、图像管理应用，替代某些核心插件
* `django-reversion`_ 1.6, 为你的内容提供版本支持

.. _django-filer: https://github.com/stefanfoulis/django-filer
.. _django CMS plugins: https://github.com/stefanfoulis/cmsplugin-filer
.. _django-reversion: https://github.com/etianen/django-reversion

在Ubuntu上安装
==============

.. warning::

    The instructions here install certain packages, such as PIL, Django, South
    and django CMS globally, which is not recommended. We recommend you use
    `virtualenv`_ instead. If you choose to do so, install Django,
    django CMS and South inside a virtualenv.

If you're using Ubuntu (tested with 10.10), the following should get you
started:

.. code-block:: bash

    sudo aptitude install python2.6 python-setuptools python-imaging
    sudo easy_install pip
    sudo pip install Django==1.4 django-cms south

Additionally, you need the Python driver for your selected database:

.. code-block:: bash

    sudo aptitude python-psycopg2

or

.. code-block:: bash

    sudo aptitude install python-mysql

This will install PIL and your database's driver globally.

You have now everything that is needed for you to follow the :doc:`tutorial`.


On Mac OSX
==========

**TODO** (Should setup everything up to but not including
"pip install django-cms" like the above)

On Microsoft Windows
====================

**TODO**.

*********
Databases
*********

We recommend using `PostgreSQL`_ or `MySQL`_ with django CMS. Installing and
maintaining database systems is outside the scope of this documentation, but is
very well documented on the systems' respective websites.

To use django CMS efficiently, we recommend:

* Creating a separate set of credentials for django CMS.
* Creating a separate database for django CMS to use.

.. _PostgreSQL: http://www.postgresql.org/
.. _MySQL: http://www.mysql.com
.. _virtualenv: http://www.virtualenv.org/
