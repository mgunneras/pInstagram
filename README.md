Instagram API Client
====================

A python client for Instagram's unofficial API. Implemented with help from [mislav's wiki notes](https://github.com/mislav/instagram/wiki/).

Depends on [restclient](http://pypi.python.org/pypi/restclient/)

Basic Usage
-----------

    from pInstagram import Instagram

    inst = Instagram()

    success, content = inst.login('username', 'password')
    if success:
        mycookie = inst.cookie #store down cookie string
        print inst.feed_timeline()

If you have a cookie stored
---------------------------

    from pInstagram import Instagram

    inst = Instagram(mycookie)

    if not inst.is_cookie_expired():
        print inst.feed_timeline()