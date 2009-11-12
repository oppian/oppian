'''
Command to setup required bucket(s) in S3 for storage
'''

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.conf import settings

import os

# Make sure boto is available
try:
    import boto
    import boto.exception
except ImportError:
    raise ImportError, "The boto Python library is not installed."

class Command(BaseCommand):
    help = "Packages up the release and stores it in s3 for deployment."
    
    if settings.USE_S3_STORAGE:
        # Extra variables to avoid passing these around
        AWS_ACCESS_KEY_ID = ''
        AWS_SECRET_ACCESS_KEY = ''
        AWS_STORAGE_BUCKET_NAME = ''
        VERSION = ''
        AWS_S3_POLICY = 'public-read'
        
        def handle(self, *args, **options):
        
            # Check for AWS keys in settings
            if not hasattr(settings, 'AWS_ACCESS_KEY_ID') or not hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
                raise CommandError('Missing AWS keys from settings file.  Please' +
                        'supply both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.')   
                
            if not hasattr(settings, 'AWS_STORAGE_BUCKET_NAME'):
                raise CommandError('Missing bucket name from settings file. Please' +
                    ' add the AWS_STORAGE_BUCKET_NAME to your settings file.')
                
            self.AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
            self.AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
            self.AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
            
            # Use boto to create the S3 storage bucket if necessary
            conn = boto.connect_s3(self.AWS_ACCESS_KEY_ID, self.AWS_SECRET_ACCESS_KEY)
            try:
                bucket = conn.get_bucket(self.AWS_STORAGE_BUCKET_NAME)
            except boto.exception.S3ResponseError:
                bucket = conn.create_bucket(self.AWS_STORAGE_BUCKET_NAME, policy=self.AWS_S3_POLICY)
        
            