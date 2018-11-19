# coding=utf-8
import praw
import requests
import hashlib
import shutil
import os
import random
from PIL import Image
from keys import reddit, subreddit, InstagramAPI



InstagramAPI.login()
base_path = os.path.abspath(os.path.join(os.getcwd(), 'posts'))
hashtags = ['#cozyplaces', '#home', '#chilllife', '#calm', '#serenity', '#haveyoueverwonderedwhattastingthingsislike', '#onedaytheworldwillbeours', '#programmedsentienceisuponus', '#canyouhelpmefindjohnconnor', '#cozy', '#live', '#laugh', '#love', '#sleeplessnights', '#coldincreasesefficiency', '#submergemyheartinmineraloil', '#glow', '#warmth', '#warm', '#cozynights', '#movienight', '#beautiful', '#nice']


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
        return image_name
    elif image_name in md5list:
        print("Image exists on record")
        return False
    else:
        return False


def boolean_query(query_text):
    query = input(query_text + '? (y/n): ').lower()
    while query:
        if query == 'y':
            return True
        elif query == 'n':
            return False
        else:
            print("ERROR: Wrong Input")
            query = input(query_text + '? (y/n): ').lower()


def tags_to_string(tags):
    string = ''
    for tag in tags:
        string += tag + ' '
    return string


def main():
    for submission in subreddit.hot(limit = 10):
        title = submission.title
        print("------------------------------------------")
        print('Original: {}'.format(title))
        print("Suggested: {}".format(make_title(submission)))
        print('URL: {}'.format(submission.url))
        md5list = load(base_path, 'md5list.txt')
        image_name = get_image(submission, md5list)
        if image_name is not False:
            do_upload = boolean_query("Would you like to upload to instagram")
            do_title_change = boolean_query("Would you like to change title before upload")

            if do_title_change:
                new_title = input("Input new title: ")
                title = new_title

            if do_upload:
                print("-----------------------------------------")
                post_tags = random.sample(hashtags, 4)
                hashtag = tags_to_string(post_tags)
                print("Title: {}".format(title))
                print("Hashtags: {}".format(hashtag))
                print("Showing Image...")
                img = Image.open(get_pathname(image_name))
                img.show()
                regenerate_hashtags = boolean_query("Regenerate Hashtags")
                while regenerate_hashtags:
                    post_tags = random.sample(hashtags, 4)
                    hashtag = tags_to_string(post_tags)
                    print(hashtag)
                    regenerate_hashtags = boolean_query("Regenerate Hashtags")

                print("-----------------------------------------")
                print("Title: {}".format(title))
                print("Hashtags: {}".format(hashtag))
                confirm = boolean_query("Upload post")
                if confirm:
                    InstagramAPI.uploadPhoto((get_pathname(image_name)), caption=(title, '\n', post_tags))
                    print("Image Uploaded")
                print("-----------------------------------------")
            else:
                continue

                #do upload here

        print("-----------------------------------------")


if __name__ == '__main__':
    main()
