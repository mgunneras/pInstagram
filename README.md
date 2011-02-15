Instagram (unofficial/private) API Client
=========================================

### Disclaimer
*Please note that Instagram strongly advices people [not to use this API endpoint for building 3rd party applications](http://www.quora.com/Instagram-told-3rd-Party-developers-today-to-stop-using-their-site-data-shutting-down-Followgram-and-possibly-others-Was-this-the-right-move-to-make-for-users). Thusly this library won't be well maintained so use it at your own discretion.*

Implemented with help from [mislav's wiki notes](https://github.com/mislav/instagram/wiki/).

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