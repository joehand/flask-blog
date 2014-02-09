from werkzeug import secure_filename
from flask.ext.security import current_user

from ..blog import Post, Article, Note
from ..utils import MarkdownReader

import StringIO
from urlparse import urlparse
import os
import zipfile
from datetime import datetime

def processMDFile(filename, contents):
    mdReader = MarkdownReader()
    contents = mdReader.read(filename, contents)

    print contents['metadata']
    print contents['content']

    slug = contents['metadata']['slug']
    kind = None
    category = None

    if 'title' in contents['metadata']:
        title = contents['metadata']['title'].strip().replace('"','')
    else:
        title = slug.replace('-', ' ').capitalize()
    
    if 'kind' in contents['metadata']:
        kind = contents['metadata']['kind']

    if 'category' in contents['metadata']:
        category = contents['metadata']['category'].strip().lower()

        if category in ['note', 'link']:
            kind = 'note'
            category = 'note'

    if kind and kind == 'page':
        post = Post(title=title, user_ref=current_user.id, kind=kind, slug=slug)

    elif kind == 'note':
        post = Note(title=title, user_ref=current_user.id, kind=kind, slug=slug)

        if 'link_url' in contents['metadata']:
            post.link_url = urlparse(contents['metadata']['link_url']).geturl()
        if 'external_link' in contents['metadata']:
            # TODO: check if there are quotes around the string
            post.link_url = urlparse(contents['metadata']['external_link']).geturl()
    else:
        post = Article(title=title, user_ref=current_user.id, kind='article', slug=slug)
        if category:
            post.category = category

    if 'published' in contents['metadata']:
        published = contents['metadata']['published']
        if published == 'true' or published is True:
            published = True
        elif published == 'false' or published is False:
            published = False
        else:
            published = False
        post.published = published


    pub_date = contents['metadata']['date']
    pub_date = datetime.strptime(pub_date.split(' ')[0], '%Y-%m-%d')
    if pub_date is not None:
        post.pub_date = pub_date

    post.content = contents['content']

    post.save()
    return post

def process_upload(files):
    if files:
        posts = []
        print files
        for file in files:
            filename = secure_filename(file.filename)
            print filename
            if filename.endswith('.zip'):
                print 'zip file!'
                zfile = zipfile.ZipFile(file)
                for name in zfile.namelist():
                    (dirname, filename) = os.path.split(name)
                    data = StringIO.StringIO(zfile.read(filename)) # convert to string IO so we can read

                    filename = os.path.splitext(filename)[0]
                    contents = data.getvalue()
                
                    post = processMDFile(filename,contents)
                    posts.append(post)
            else:
                filename = os.path.splitext(filename)[0]
                contents = file.read()
                
                post = processMDFile(filename,contents)
                posts.append(post)
                file.close()

        return posts

