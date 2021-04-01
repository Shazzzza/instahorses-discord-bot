import instalogin
import random
import datetime


class Post:
    IMAGE_INDEX = 0
    THUMBNAIL_INDEX = 1

    def __init__(self, post):
        self.post = post;

    def get_url(self) -> str:
        return f'https://instagram.com/p/{self.post["code"]}'

    def get_description(self) -> str:
        return self.post['caption']['text']

    def get_profile_name(self) -> str:
        return self.post['user']['full_name']

    def get_profile_url(self) -> str:
        return f'https://instagram.com/{self.post["user"]["username"]}'

    def get_profile_picture_url(self) -> str:
        return self.post['user']['profile_pic_url']

    def get_timestamp(self) -> datetime:
        return datetime.datetime.utcfromtimestamp(self.post['taken_at'])

    def get_image_url(self) -> str:
        return self.get_img_data(self.IMAGE_INDEX)['url']

    def get_thumbnail_url(self) -> str:
        return self.get_img_data(self.THUMBNAIL_INDEX)['url']

    def get_img_data(self, index) -> dict:
        image = self.post['image_versions2']['candidates'][index]
        return {
            'height': image['height'],
            'width': image['width'],
            'url': image['url'],
        }


class HashtagSearch:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api = instalogin.login(username, password)

    def get_random_post_for_hashtag(self, tag) -> Post:
        # api = instalogin.login(self.username, self.password)
        results = self.api.feed_tag(tag, self.api.generate_uuid())
        items = results.get('ranked_items', [])
        if len(items) == 0:
            raise Exception(f'No posts found for #{tag}')

        if len(items) == 1:
            return Post(items[0])

        index = random.randint(0, len(items) - 1)
        return Post(items[index])

#
# if __name__ == "__main__":
#     print(get_random_post_for_hashtag('horses'))
