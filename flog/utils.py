from __future__ import unicode_literals
from datetime import datetime
from hashlib import sha1
import json
import re
import six

import boto
from flask import current_app as app
from flask import Markup
from markdown import Markdown
from werkzeug import secure_filename

from .extensions import db

# Global Vars
META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')
META_MORE_RE = re.compile(r'^[ ]{4,}(?P<value>.*)')

def s3_signer(request):

        AWS_ACCESS_KEY = current_app.config['AWS_ACCESS_KEY_ID']
        AWS_SECRET_KEY =  current_app.config['AWS_SECRET_ACCESS_KEY']
        S3_BUCKET =  current_app.config['S3_BUCKET_NAME']

        object_name = request.args.get('s3_object_name')
        mime_type = request.args.get('s3_object_type')

        expires = int(time.time()+20)
        amz_headers = 'x-amz-acl:public-read'

        put_request = 'PUT\n\n%s\n%d\n%s\n/%s/%s' % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

        signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
        signature = urllib.quote_plus(signature.strip())

        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

        return json.dumps({
            'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' \
                % (url, AWS_ACCESS_KEY, expires, signature),
            'url': url
            })

def s3_upload(filename, contents ,acl='public-read'):
    ''' From: https://github.com/doobeh/Flask-S3-Uploader/blob/master/tools.py

        Uploads WTForm File Object to Amazon S3

        Expects following app.config attributes to be set:
            AWS_ACCESS_KEY_ID       :   S3 API Key
            AWS_SECRET_ACCESS_KEY   :   S3 Secret Key
            S3_BUCKET_NAME          :   What bucket to upload to
            S3_UPLOAD_DIRECTORY     :   Which S3 Directory.

        The default sets the access rights on the uploaded file to
        public-read.  It also generates a unique filename via
        the uuid4 function combined with the file extension from
        the source file.
    '''
    # Connect to S3 and upload file.
    conn = boto.connect_s3(app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
    b = conn.get_bucket(app.config['S3_BUCKET_NAME'])

    sml = b.new_key('/'.join([app.config['S3_UPLOAD_DIRECTORY'],filename]))
    sml.set_contents_from_string(contents)
    sml.set_acl(acl)

    return sml.generate_url(expires_in=300, query_auth=False)


class MarkdownReader():
    '''
    Reader for Markdown files

    Modified from Pelican and Python Markdown
    '''
    def process_filename(self, filename):
        m = re.search(r'(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)', filename).groupdict()
        return m

    def getmeta(self, lines):
        ''' Parse Meta-Data 

            From python markdown meta extension
        '''
        meta = {}
        key = None
        while lines:
            line = lines.pop(0)
            if line.strip() == '':
                break # blank line - done
            m1 = META_RE.match(line)
            if m1:
                key = m1.group('key').lower().strip()
                value = m1.group('value').strip()
                try:
                    meta[key].append(value[0])
                except KeyError:
                    meta[key] = [value][0]
            else:
                m2 = META_MORE_RE.match(line)
                if m2 and key:
                    # Add another line to existing key
                    meta[key].append(m2.group('value').strip()[0])
                else:
                    lines.insert(0, line)
                    break # no meta data - done
        return meta

    def read(self, filename, contents):
        '''Parse content and metadata of markdown files'''
        contents = contents.replace('\r', '')
        metadata = contents.split('\n\n',1)[0]
        metadata = self.getmeta(metadata.split('\n'))

        content = contents.split('\n\n',1)[1]
        content = re.sub(r'(?<!\n)\n(?!\n)', ' ', content) # replace single newline characters with spaces

        metadata.update(self.process_filename(filename))
        return {'content':content, 'metadata':metadata}

def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%d-%b-%Y')
    except ValueError:
        raise ValueError('Incorrect data format')

def slugify(value, substitutions=()):
    '''
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Took from Django sources.
    '''
    # TODO Maybe steal again from current Django 1.5dev
    value = Markup(value).striptags()
    # value must be unicode per se
    import unicodedata
    from unidecode import unidecode
    # unidecode returns str in Py2 and 3, so in Py2 we have to make
    # it unicode again
    value = unidecode(value)
    if isinstance(value, six.binary_type):
        value = value.decode('ascii')
    # still unicode
    value = unicodedata.normalize('NFKD', value).lower()
    for src, dst in substitutions:
        value = value.replace(src.lower(), dst.lower())
    value = re.sub('[^\w\s-]', '', value).strip()
    value = re.sub('[-\s]+', '-', value)
    # we want only ASCII chars
    value = value.encode('ascii', 'ignore')
    # but Pelican should generally use only unicode
    return value.decode('ascii')

def mongo_to_dict(obj):
    return_data = []

    if isinstance(obj, db.DynamicDocument):
        return_data.append(('id',str(obj.id)))
    if isinstance(obj, db.Document):
        return_data.append(('id',str(obj.id)))

    for field_name in obj._fields:

        if field_name in ('id',):
            continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], db.DateTimeField):
            if data:
                return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], db.StringField):
            try:
                data = str(data)
            except:
                data = data
                pass
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name], db.FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], db.BooleanField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], db.IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], db.ListField):
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name], db.EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data)))
        elif isinstance(obj._fields[field_name], db.DictField):
            return_data.append((field_name, data))

    return dict(return_data)