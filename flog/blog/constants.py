
ILLEGAL_SLUGS = ['admin', 'archives', 'category']

POST_TYPES = (('article','Article'),
              ('note','Note'), 
              ('page','Page'))

# keys to accept over PUT request (used for validation)
ACCEPTED_KEYS = ['title', 'slug', 'content', 'published', 
                    'kind', 'link_url', 'pub_date', 'category']

