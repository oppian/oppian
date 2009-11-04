import os

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.functional import curry
from django.core.exceptions import ImproperlyConfigured

try:
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
except ImportError:
    raise ImproperlyConfigured, "Could not load Boto's S3 bindings.\
    \nSee http://code.google.com/p/boto/"

ACCESS_KEY_NAME = 'AWS_ACCESS_KEY_ID'
SECRET_KEY_NAME = 'AWS_SECRET_ACCESS_KEY'
HEADERS = 'AWS_HEADERS'
BUCKET_NAME = 'AWS_STORAGE_BUCKET_NAME'
DEFAULT_ACL = 'AWS_DEFAULT_ACL'
QUERYSTRING_AUTH = 'AWS_QUERYSTRING_AUTH'
QUERYSTRING_EXPIRE = 'AWS_QUERYSTRING_EXPIRE'

BUCKET_PREFIX = getattr(settings, BUCKET_NAME, {})
HEADERS = getattr(settings, HEADERS, {})
DEFAULT_ACL = getattr(settings, DEFAULT_ACL, 'public-read')
QUERYSTRING_AUTH = getattr(settings, QUERYSTRING_AUTH, True)
QUERYSTRING_EXPIRE = getattr(settings, QUERYSTRING_EXPIRE, 3600)


class S3BotoStorage(Storage):
    """Amazon Simple Storage Service using Boto"""

    def __init__(self, bucket="root", bucketprefix=BUCKET_PREFIX,
            access_key=None, secret_key=None, acl=DEFAULT_ACL, headers=HEADERS):
        self.acl = acl
        self.headers = headers

        if not access_key and not secret_key:
             access_key, secret_key = self._get_access_keys()

        self.connection = S3Connection(access_key, secret_key)
        self.bucket = self.connection.create_bucket(bucketprefix + bucket)
        self.bucket.set_acl(self.acl)

    def _get_access_keys(self):
        access_key = getattr(settings, ACCESS_KEY_NAME, None)
        secret_key = getattr(settings, SECRET_KEY_NAME, None)
        if (access_key or secret_key) and (not access_key or not secret_key):
            access_key = os.environ.get(ACCESS_KEY_NAME)
            secret_key = os.environ.get(SECRET_KEY_NAME)

        if access_key and secret_key:
            # Both were provided, so use them
            return access_key, secret_key

        return None, None

    def _clean_name(self, name):
        # Useful for windows' paths
        return os.path.normpath(name).replace('\\', '/')

    def _open(self, name, mode='rb'):
        name = self._clean_name(name)
        return S3BotoProxyStorageFile(name, mode, self)

    def _save(self, name, content):
        name = self._clean_name(name)
        headers = self.headers
        if hasattr(content.file, 'content_type'):
            headers['Content-Type'] = content.file.content_type
        content.name = name
        k = self.bucket.get_key(name)
        if not k:
            k = self.bucket.new_key(name)
        k.set_contents_from_file(content, headers=headers, policy=self.acl)
        return name

    def delete(self, name):
        name = self._clean_name(name)
        self.bucket.delete_key(name)

    def exists(self, name):
        name = self._clean_name(name)
        k = Key(self.bucket, name)
        return k.exists()

    def listdir(self, name):
        name = self._clean_name(name)
        ret_arr = []
        for l in self.bucket.list(prefix=name+'/', delimiter='/'):
            tmpname = l.name[len(name) + 1:]
            if not len(name) or l.name[:len(name)] == name:
                ret_arr.append(tmpname)
        return ret_arr
        #return [l.name[len(name) + 1:] for l in self.bucket.list() if not len(name) or l.name[:len(name)] == name]

    def size(self, name):
        name = self._clean_name(name)
        key = self.bucket.get_key(name)
        if key:
            return key.size
        return 0 # folders are not found independently of files and are set to have 0 size
    
    def last_modified(self, name):
        name = self._clean_name(name)
        key = self.bucket.get_key(name)
        import time
        import datetime
        if key:
            last_modified_str = key.last_modified
            return datetime.datetime(*time.strptime(
                            last_modified_str, '%a, %d %b %Y %H:%M:%S %Z')[0:6])
        return datetime.datetime.now()
        
    def url(self, name):
        name = self._clean_name(name)
        return self.bucket.get_key(name).generate_url(QUERYSTRING_EXPIRE, method='GET', query_auth=QUERYSTRING_AUTH)

    def get_available_name(self, name):
        """ Overwrite existing file with the same name. """
        name = self._clean_name(name)
        return name


class S3BotoStorageFile(File):
    def __init__(self, name, mode, storage):
        self._storage = storage
        self._name = name
        self._mode = mode
        self.key = storage.bucket.get_key(name)

    def size(self):
        return self.key.size

    def read(self, *args, **kwargs):
        return self.key.read(*args, **kwargs)

    def write(self, content):
        self.key.set_contents_from_string(content, headers=self._storage.headers, acl=self._storage.acl)

    def close(self):
        self.key.close()

    def seek(self, pos):
        if pos == 0:
            self.close()
            self.key = self._storage.bucket.get_key(self._name)
        else:
            raise NotImplemented

from django.core.files.temp import NamedTemporaryFile

class S3BotoProxyStorageFile(File):
    def __init__(self, name, mode, storage):
        self._storage = storage
        self._name = name
        self._mode = mode
        self.key = storage.bucket.get_key(name)
        # create tmp file and write key to it
        tmpfile = NamedTemporaryFile(mode="w+b", suffix=os.path.splitext(name)[1])
        self.key.open()
        for chunk in self.key:
            tmpfile.write(chunk)
        tmpfile.seek(0)
        self.tmpfile = tmpfile
        self.file = tmpfile.file

    def tell(self):
        return self.tmpfile.file.tell()


    def size(self):
        return self.tmpfile.size

    def read(self, *args, **kwargs):
        return self.tmpfile.read(*args, **kwargs)

    def write(self, content):
        self.key.set_contents_from_string(content, headers=self._storage.headers, acl=self._storage.acl)
        # TODO: fix delete of local file

    def close(self):
        self.tmpfile.close()

    def seek(self, pos):
        return self.tmpfile.seek(pos)

