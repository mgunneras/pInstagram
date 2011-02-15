#!/usr/bin/env python
# encoding: utf-8

import json
import datetime

from restclient import GET, POST
# pip install -e git+https://github.com/thraxil/restclient.git#egg=restclient

COOKIE_DATEFORMAT = "%a, %d-%b-%Y %H:%M:%S GMT"
BASE_URL = 'http://instagr.am/api/v1'
USER_AGENT = 'pInstagram'

class CookieException(Exception): pass
class APIError(Exception): pass

def get_cookie_expiry_datetime(cookie):
    """
    example cookie:
    sessionid=XXXXXXXXXXXXXXXXXXXXX; expires=Wed, 16-Mar-2011 17:52:10 GMT; Max-Age=2592000; Path=/, ds_user=USERNAME; Max-Age=2592000; Path=/, ds_user_id=USERID; Max-Age=2592000; Path=/
    """
    try:
        start = cookie.lower().find('expires') + 8
        date = cookie[start:start+29]
        return datetime.datetime.strptime(date, COOKIE_DATEFORMAT)
    except Exception, e:
        raise CookieException('Error parsing cookie data')

def standard_response(fn):
    def inner(*args, **kwargs):
        success, rsp, json_content = fn(*args, **kwargs)
        return success, json_content
    return inner

class Instagram(object):
    
    def __init__(self, cookie=None):
        if cookie:
            self.set_cookie(cookie)

    def set_cookie(self, cookie):
        self.cookie_expires = get_cookie_expiry_datetime(cookie)
        self.cookie = cookie

    def is_cookie_expired(self):
        return self.cookie_expires < datetime.datetime.now()

    def check_cookie(self):
        if hasattr(self, 'cookie') and not self.is_cookie_expired():
            return True
        else:
            raise CookieException

    def login(self, username, password, device_id='0000'):
        success, rsp, json_content = self._invoke('/accounts/login/', POST, False, params={'username':username, 'password':password, 'device_id':device_id})
        if success:
            self.set_cookie(rsp['set-cookie'])
        return success, json_content

    @standard_response
    def logout(self):
        return self._invoke('/accounts/logout/', GET, True)

    @standard_response
    def activity_recent(self):
        """Users activity stream (news)"""
        return self._invoke('/activity/recent/', GET, True)

    @standard_response
    def feed_timeline(self):
        """Users timeline"""
        return self._invoke('/feed/timeline/', GET, True)

    @standard_response
    def feed_popular(self):
        """Users timeline"""
        return self._invoke('/feed/popular/', GET, True)

    @standard_response
    def feed_location(self, location_pk):
        return self._invoke('/feed/location/%s/' % location_pk, GET, False)

    @standard_response
    def feed_tag(self, tag, max_id=0):
        return self._invoke('/feed/tag/%s/' % tag, GET, False, params={'max_id':max_id})

    @standard_response
    def tags_search(self, query):
        return self._invoke('/tags/search/', GET, False, params={'q':query})

    @standard_response
    def tag_info(self, tag):
        return self._invoke('/tags/%s/info/' % tag, GET, False)




    def _invoke(self, path, method, require_cookie, **kwargs):
        url = "%s%s" % (BASE_URL, path)

        rest_defaults = {
            'async': False,
            'resp': True,
            'headers' : {
                'User-Agent' : USER_AGENT
            },
        }

        rest_defaults.update(kwargs)

        if require_cookie:
            self.check_cookie()
            rest_defaults['headers'].update({
                'Cookie' : self.cookie
            })

        rsp, content = method(url, **rest_defaults)

        try:
            json_content = json.loads(content)
        except:
            raise APIError('Instagram API did not return json string: %s' % content)

        success = json_content['status'] == 'ok'

        if not success and json_content['message'] == 'login_required':
            raise CookieException('Login required')

        return success, rsp, json_content
