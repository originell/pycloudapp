==========
pycloudapp
==========

is
--

a wrapper around the CloudApp_ api_.

Requirements
============

- Python >= 2.5

In order to upload files you need to have:
    - poster_
    - ordereddict_
    
Both of these are available in pypi.

HowTo
=====

    >>> from pycloudapp.cloud import Cloud
    >>> mycloud = Cloud()
    >>> mycloud.auth('yourusername', 'yourpassword')
    >>> mycloud.upload_file('somefile.png')

License
=======

See LICENSE.

.. _CloudApp: http://www.getcloudapp.com/
.. _api: http://support.getcloudapp.com/faqs/developers/api
.. _poster: http://atlee.ca/software/poster/
.. _ordereddict: http://pypi.python.org/pypi/ordereddict/1.1
