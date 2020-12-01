import os
import ujson
import sqlite3
import bilibili_api as bi

def get_old_followers() -> list:
    return old_followers

def diff_followers(followers: list, old_follwors: list):
    new_follow = list(set(followers) - set(old_follwors))
    new_unfollow = list(set(old_followers) - set(followers))
    return new_follow, new_unfollow

def write_into_db(conn, new_follow, new_unfollow) -> None:
    raise NotImplementedError

def read_old_from_db() -> list:


if __name__ == "__main__":

    resource_dir = os.getcwd()

    with open(os.path.join(resource_dir,'xc_info.json')) as f:
        xc_info = ujson.load(f)

    uid = xc_info.get('uid')
    sessdata = xc_info.get('sessdata')

    followers = bi.user.get_followers(uid=uid, sessdata=sessdata)
    old_followers = get_old_followers()
    


    