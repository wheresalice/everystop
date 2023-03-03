from mastodon import Mastodon
from everystop import get_random_stop, mark_visited


mastodon = Mastodon(
    access_token='pytooter_usercred.secret',
    api_base_url='https://botsin.space'
)

record = get_random_stop()

media = mastodon.media_post('sv.jpg')
post = mastodon.status_post(record['name'], media_ids=media)

mark_visited(record['id'], post['url'])
