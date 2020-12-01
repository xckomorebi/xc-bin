import os
import ujson
import sqlite3
import bilibili_api as bi


def get_followers(uid: str) -> list:
    bi.common.get_comments


def get_old_followers(uid: ):
    raise NotImplementedError

def diff_followers():
    raise NotImplementedError

def write_into_db():
    raise NotImplementedError

def read_old_from_db() -> list:


if __name__ == "__main__":

    resource_dir = os.getcwd()

    with open(os.path.join(resource_dir,'xc_info.json')) as f:
        xc_info = ujson.load(f)

    uid = xc_info.get('uid')

    followers = get_followers(uid)

    