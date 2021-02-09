import json
from pyfacebook import Api
api = Api(
        app_id = "692001264799472",
        app_secret = "60b272a45b500fef45f3c930d5d6d8df",
        long_term_token = "EAAJ1XxmSjvABAIVSXdbeDkCVQuewmUMOs8ZClysBW8NWZBMx3zGR2wN3EWZBUwjlUfSh2NF7jDztlXSALCal8VYjGZAd69wZA0xd5XUBJpB6YY3bcZC1SZBV7juZCpnBHHdc8X6ZBN1O6CjAZBt9nWPZC4BY1v0KJfRGkhpRvXjiaZA1oPS90vt6HJcRIynEvxDadJsZD",
        )
def get_posts(page_id):  
    data = api.get_page_posts(
        page_id=page_id,
        since_time="2020-05-01",
        count=None,
        limit=100,
        return_json=True,
    )
    return data


def processor():
    page_id = "341526406956810"
    data = get_posts(page_id)
    with open("wto_posts.json", 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    processor()
