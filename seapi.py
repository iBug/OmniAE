import requests
import html

import core


class Post:
    __getitem__ = getattr
    __setitem__ = setattr

    def __init__(self):
        self.id = None
        self.url = None
        self.type = None
        self.site = None
        self.owner_url = None
        self.owner_name = None
        self.owner_rep = None
        self.title = None
        self.body = None
        self.raw_body = None
        self.score = None
        self.upvote = None
        self.downvote = None
        self.question_id = None
        self.creation_date = None
        self.last_edit_date = None


def get_post(site, post_id, post_type):
    """
    Fetch a post from the Stack Exchange API
    """
    if post_type == "answer":
        api_filter = r"!FdmhxNRjn0vYtGOu3FfS5xSwvL"
    elif post_type == "question":
        api_filter = r"!DEPw4-PqDduRmCwMBNAxrCdSZl81364qitC3TebCzqyF4-y*r2L"
    else:
        raise ValueError("post_type must be either 'question' or 'answer'")

    api_filter = r"!*1SdVEqS-F*E3oCZH7zp*8EkDYoKq98j9rjbmSU4y"
    request_url = "https://api.stackexchange.com/2.2/{}s/{}".format(post_type, post_id)
    params = {
        'filter': api_filter,
        'key': core.config.read_key,
        'site': site,
    }
    response = requests.get(request_url, params=params).json()
    try:
        item = response['items'][0]
    except (KeyError, IndexError):
        print(response)
        return None

    post = Post()
    post.id = post_id
    post.url = item['share_link']
    post.type = post_type
    post.title = html.unescape(item['title'])
    if 'owner' in item and 'link' in item['owner']:
        post.owner_name = html.unescape(item['owner']['display_name'])
        post.owner_url = item['owner']['link']
        post.owner_rep = item['owner']['reputation']
    else:
        post.owner_name = ""
        post.owner_url = ""
        post.owner_rep = 1
    post.site = site
    post.body = item['body']
    post.score = item['score']
    post.upvotes = item['up_vote_count']
    post.downvotes = item['down_vote_count']
    post.creation_date = item['creation_date']
    post.last_edit_date = item.get('last_edit_date', post.creation_date)
    if post_type == "answer":
        post.question_id = item['question_id']
    else:
        post.question_id = post_id
    return post
