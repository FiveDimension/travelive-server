__author__ = 'jian.zhang'

import time


def create_id(user_id):
    return str(user_id) + str(int(time.time()))


if __name__ == "__main__":
    id = create_id(23)
    print id

