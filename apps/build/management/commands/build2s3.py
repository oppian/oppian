"""
Sync Media to S3
================

Django command that creates a tar.gz of all the files in the project dir 
and then uploads that to s3.

"""

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django_extensions.management.utils import get_project_root
from django.conf import settings

from tempfile import TemporaryFile
import os


# Make sure boto is available
try:
    import boto
    import boto.exception
except ImportError:
    raise ImportError, "The boto Python library is not installed."

def get_base_dir():
    return get_project_root()

def list_files(dir, file_list):
    """Loops through all files ignore dot and pyc files."""
    filecount = 0
    for filename in os.listdir(dir):
        if filename.startswith('.'):
            continue
        if filename.endswith('.pyc'):
            continue
        if filename.endswith('.bak'):
            continue
        if filename.startswith('settings_local'):
            continue
        fullname = os.path.join(dir, filename)
        # test if in ignore
        if fullname in settings.BUILD_IGNORE:
            continue
        if os.path.isdir(fullname):
            filecount = filecount + list_files(fullname, file_list)
            continue
        file_list.append(fullname)
        print " + %s" % fullname
        filecount = filecount + 1
    return filecount
        
def create_tmp(suffix=None):
    """Creates a tmp file with a particular prefix and suffix."""
    return TemporaryFile(prefix='%s-git-' % settings.BUILD_APPNAME, suffix=suffix)

def targz_files(file_list):
    """Tars and gzips files from file_list. Returns the .tar.gz file."""
    import tarfile
    tmpfile = create_tmp('.tar.gz')
    print "Creating %s file archive..." % tmpfile.name
    file_targz = tarfile.open(mode='w:gz', fileobj=tmpfile)
    basedir = get_base_dir()
    os.chdir(basedir)
    for filename in file_list:
        if filename.startswith(basedir):
            filename = filename[len(basedir)+1:]
        file_targz.add(filename)
    file_targz.close()
    return tmpfile

class Command(BaseCommand):
    help = "Packages up the release and stores it in s3 for deployment."
    
    # Extra variables to avoid passing these around
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_BUILD_BUCKET_NAME = ''
    VERSION = ''
    
    def handle(self, *args, **options):
    
        # Check for AWS keys in settings
        if not hasattr(settings, 'AWS_ACCESS_KEY_ID') or not hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
            raise CommandError('Missing AWS keys from settings file.  Please' +
                    'supply both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.')

            
        if not hasattr(settings, 'AWS_BUILD_BUCKET_NAME'):
            raise CommandError('Missing bucket name from settings file. Please' +
                ' add the AWS_BUILD_BUCKET_NAME to your settings file.')
        else:
            if not settings.AWS_BUILD_BUCKET_NAME:
                raise CommandError('AWS_BUILD_BUCKET_NAME cannot be empty.')
            
        self.AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
        self.AWS_BUILD_BUCKET_NAME = settings.AWS_BUILD_BUCKET_NAME
        
        # create the version string
        self.save_version()
        
        # create a list of files to archive
        file_list = []
        print "Creating list of files..."
        filecount = list_files(get_base_dir(), file_list)
        print "%d Files added" % filecount
        
        # tar and gzip list
        file_targz = targz_files(file_list)
        
        # upload to s3
        self.upload_s3(file_targz)
        # close file to delete it
        file_targz.close()
        
    def save_version(self):
        """Creates a version string and saves it to a text file"""
        from datetime import datetime
        self.VERSION = '%s-%s.%s-%s' % (settings.BUILD_APPNAME, 
            settings.BUILD_VERSION[0], settings.BUILD_VERSION[1], 
            datetime.now().strftime('%Y%m%d%H%M%S'))
        ver_file = open(os.path.join(get_project_root(), 'templates', 'VERSION.txt'), 'w')
        ver_file.write(self.VERSION)
        ver_file.close()
     
    def upload_s3(self, file_archive):
        """Uploads a file to s3"""
        
        # first open the s3 connection
        bucket = self.open_s3()
        key = boto.s3.key.Key(bucket)
        
        # set key name
        key.name = "%s.tar.gz" % self.VERSION
        
        # now upload
        def upload_cb(bytes_done, bytes_togo):
            if bytes_togo > 0:
                percent = (bytes_done * 100) / bytes_togo
                print '%s%%' % percent 
            
        print "Uploading %s..." % (key.name)
        key.set_contents_from_file(file_archive, cb=upload_cb)
        
 
    def open_s3(self):
        """
        Opens connection to S3 returning bucket and key
        """
        conn = boto.connect_s3(self.AWS_ACCESS_KEY_ID, self.AWS_SECRET_ACCESS_KEY)
        try:
            bucket = conn.get_bucket(self.AWS_BUILD_BUCKET_NAME)
        except boto.exception.S3ResponseError:
            bucket = conn.create_bucket(self.AWS_BUILD_BUCKET_NAME)
        return bucket    