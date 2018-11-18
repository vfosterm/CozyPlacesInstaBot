# coding=utf-8
import praw
import requests
import hashlib
import shutil
import os
from keys import reddit, subreddit

base_path = os.path.abspath(os.path.join(os.getcwd(), 'posts'))


# remember to add file creation try/except
def load(path, name):
    list = []
    filename = get_pathname(name)
    if os.path.exists(path):
        with open(filename) as fin:
            for entry in fin.readlines():
                list.append(entry.rstrip())
    return list


def save(name, data):
    filename = get_pathname(name)
    with open(filename, 'a') as fout:
        fout.write(data + '\n')


def save_image(path, name, data):
    filename = os.path.join(path, name)
    with open(filename, 'wb') as fout:
        shutil.copyfileobj(data, fout)


def get_pathname(name):
    filename = os.path.abspath(os.path.join(base_path, name))
    return filename


def is_personal(string):
    title = string.lower().split()
    if ("my" or "our") in title:
        return True
    else:
        return False


def make_title(submission):
    title = submission.title
    if not is_personal(title):
        return title.rstrip()
    else:
        if ('My' or 'Our') in title.split():
            title = title.replace('My', 'A').replace('Our', 'A')
        elif ('my' or 'our') in title.split():
            title = title.replace('my', 'a').replace('our', 'a')
        return title


def make_comments(submission):
    submission.comments.replace_more(limit=0)
    submission.comments.comment_sort = 'top'
    comments = submission.comments.list()


def is_image(url):
    if ".jpg" or ".png" in url:
        return True
    else:
        return False


def get_image(submission, md5list):
    url = submission.url
    image_name = hashlib.md5(str(url).encode('utf-8')).hexdigest()

    if is_image(url) and image_name not in md5list:
        response = requests.get(url, stream=True)
        image_data = response.raw
        save('md5list.txt', image_name)
        save_image(base_path, image_name, image_data)
        print('success')
    elif image_name in md5list:
        print("Image exists on record")
        return False
    else:
        return False


def main():
    for submission in subreddit.hot(limit = 10):
        title = submission.title
        print("------------------------------------------")
        print('Original: {}'.format(title))
        print("Suggested: {}".format(make_title(submission)))
        print('URL: {}'.format(submission.url))
        md5list = load(base_path, 'md5list.txt')
        get_image(submission, md5list)
        print("-----------------------------------------")


if __name__ == '__main__':
    main()
