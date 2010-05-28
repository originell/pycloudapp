import urllib2
import urllib
import json
import os

# Python does not support multipart/form-data encoding out of the box
FILE_UPLOAD = 1
try:
    import poster
except ImportError:
    print 'Poster is not installed. Fileupload disabled.'
    FILE_UPLOAD = 0

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
else:
    print 'Neither Python 2.7 nor ordereddict is installed. Fileupload disabled.'
    FILE_UPLOAD = 0

__version__ = 'beta'

PROTOCOL = 'http://'
    
URI = 'cl.ly'
AUTH_URI = 'my.cl.ly'
USER_AGENT = 'Cloud API Python Wrapper/%s' % __version__

FILE_TYPES = ('image', 'bookmark', 'test', 'archive', 'audio', 'video', 'unknown')


class CloudException(Exception):
    pass

class DeleteRequest(urllib2.Request):
    def get_method(self):
        return "DELETE"

class Cloud(object):
    def __init__(self):
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-Agent', USER_AGENT),
                                  ('Accept', 'application/json'),]
        self.auth_success = 0

    def auth(self, username, password):
        passwordmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwordmgr.add_password(None, AUTH_URI, username, password)
        auth = urllib2.HTTPDigestAuthHandler(passwordmgr)

        self.auth_opener = urllib2.build_opener(auth)
        self.auth_opener.addheaders = [('User-Agent', USER_AGENT),
                                       ('Accept', 'application/json'),]

        if FILE_UPLOAD:
            self.upload_auth_opener = poster.streaminghttp.register_openers()
            self.upload_auth_opener.add_handler(auth)
            self.upload_auth_opener.addheaders = [('User-Agent', USER_AGENT),
                                                  ('Accept', 'application/json'),]

        if self.auth_success == 0:
            self._test_auth()

    def _test_auth(self):
        query = urllib.urlencode({'page': 1, 'per_page': 1})
        page = self.auth_opener.open('%s%s/items?%s' % (PROTOCOL, AUTH_URI, query))
        if page.code == 200:
            self.auth_success = 1
            return True
        raise False

    def item_info(self, uri):
        validator = '%s%s' % (PROTOCOL, URI)
        if validator in uri:
            return json.load(self.opener.open(uri))
        return False

    def list_items(self, page=False, per_page=False, file_type=False, deleted=False):
        if self.auth_success == 0:
            raise CloudException('Not authed')
        
        params = {}
        if page:
            params['page'] = int(page)
        if per_page:
            params['per_page'] = int(per_page)
        if file_type:
            if isinstance(file_type, basestring) and \
               file_type.lower() in FILE_TYPES:
                params['type'] = file_type
        if deleted:
            params['deleted'] = bool(deleted)

        query = urllib.urlencode(params)
        return json.load(self.auth_opener.open('%s%s/items?%s' % (PROTOCOL, AUTH_URI, query)),
                         encoding='utf-8')

    def create_bookmark(self, name, bookmark_uri):
        if self.auth_success == 0:
            raise CloudException('Not authed')

        #values = {'name': name, 'redirect_url': bookmark_uri}
        #data = urllib.urlencode(values)
        values = {'item': {'name': name, 'redirect_url': bookmark_uri}}
        data = json.dumps(values, encoding='utf-8')
        request = urllib2.Request('%s%s/items' % (PROTOCOL, AUTH_URI), data)
        request.add_header('Content-Type', 'application/json')

        return json.load(self.auth_opener.open(request))

    def upload_file(self, path):
        if FILE_UPLOAD == 0:
            raise CloudException('Fileupload has been disabled as "poster" or'\
                                 '"ordereddict" is not installed.')
        if self.auth_success == 0:
            raise CloudException('Not authed')

        if not os.path.exists(path):
            raise CloudException('File does not exist')
        if not os.path.isfile(path):
            raise CloudException('The given path does not point to a file')

        directives = json.load(self.auth_opener.open('%s%s/items/new' % (PROTOCOL, AUTH_URI)))
        directives['params']['key'] = directives['params']['key'] \
                                      .replace('${filename}',
                                               os.path.split(path)[-1])
        upload_values = OrderedDict(sorted(directives['params'].items(), key=lambda t: t[0]))
        upload_values['file'] = open(path, 'rb').read()
        datagen, headers = poster.encode.multipart_encode(upload_values)
        request = urllib2.Request(directives['url'], datagen, headers)

        return json.load(self.upload_auth_opener.open(request))

    def delete_file(self, href):
        if self.auth_success == 0:
            raise CloudException('Not authed')
        result = self.auth_opener.open(DeleteRequest(href))
        if result.code == 200:
            return True
        raise CloudException('Deletion of failed')
