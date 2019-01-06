from instagram_private_api import Client, ClientCompatPatch
import json, wget, yaml, time, random

with open('settings.yaml') as settings:
    settings = yaml.load(settings)

hashtags = settings['hashtags']
user_name = settings['username']
password = settings['password']

print("we gonna check such hashtags:",hashtags)

api = Client(user_name, password)

for tag in hashtags:
    rank_token = api.generate_uuid()
    print("============ retrieved new rank_token:",rank_token,"for",tag," ============")
    results = api.feed_tag(tag, rank_token)
    if results.get('story'):    # Returned only in version >= 10.22.0
        items = [item for item in results.get('story', []).get('items', [])
        if item.get('media_type') == 2 ]
        for item in items:
            print("\ncode:",item['code'],"url:",item['video_versions'][0]['url'])
            url = item['video_versions'][0]['url']
            wget.download(url, './content/')
            time.sleep(random.choice([0, 1, 2]))
        print("\n============ end of ",tag," ============")
