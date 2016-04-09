__author__ = 'jian.zhang'

import time
import hashlib


def create_id(user_id):
    return str(user_id) + str(int(time.time()))


def get_hash(username):
    return int(hashlib.sha1(username).hexdigest(), 16) % (10 ** 8)


if __name__ == "__main__":
    id = create_id(23)
    print id

