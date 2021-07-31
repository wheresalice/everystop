from mastodon import Mastodon

Mastodon.create_app(
    'pytooterapp',
    api_base_url='https://botsin.space',
    to_file='pytooter_clientcred.secret'
)

mastodon = Mastodon(
    client_id='pytooter_clientcred.secret',
    api_base_url='https://botsin.space'
)
mastodon.log_in(
    'your_email@example.net',
    'supers3cr3tpassword',
    to_file='pytooter_usercred.secret'
)
