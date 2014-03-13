ILLEGAL_SLUGS = ['admin', 'archives', 'category']

POST_TYPES = (('article','Article'),
              ('note','Note'),
              ('page','Page'))

# keys to accept over PUT request (used for validation)
ACCEPTED_KEYS = ['title', 'subtitle', 'slug', 'content', 'published',
                    'kind', 'link_url', 'pub_date', 'category']

# Keys to export to MD file
EXPORT_KEYS = ['title', 'kind', 'category', 'link_url', 'published',
                'slug', 'pub_date', 'last_update']

ALLOWED_COMMENT_TAGS = ['a', 'p','em','strong',
                        'code','pre','blockquote']
