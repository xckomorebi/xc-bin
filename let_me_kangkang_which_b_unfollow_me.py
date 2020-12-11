import os
import ujson
import sqlite3
import bilibili_api as bi
import logging

from pync import notify

# ugly, but it works

logger = logging.getLogger("fan_tracer")
logging.basicConfig(filename='bin/resource/fan_tracer.log', filemode='a',
                    level=logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%m/%d/%Y %H:%M:%S' )

def get_old_followers(c):
    c.execute("SELECT * FROM follower ORDER BY id DESC LIMIT 1;")
    old_followers = c.fetchone()[1].split(',')
    return old_followers


def diff_followers(followers: list, old_followers: list):
    new_follow = list(set(followers) - set(old_followers))
    new_unfollow = list(set(old_followers) - set(followers))
    return new_follow, new_unfollow


def followers_filter(resp):
    followers_raw = []
    followers = []
    for follower in resp:
        followers_raw.append((follower.get('mid'), follower.get('uname')))
        followers.append(follower.get('mid'))
    followers = list(map(str,followers))
    return followers_raw, followers


def get_name_by_uid(uid: str):
    uid = int(uid)
    name = bi.user.get_user_info(uid).get('name')
    return name


def handle_unfollower(c, un_follower):
    unfollower_name = []
    for follower in un_follower:
        name = get_name_by_uid(follower)
        c.execute("select * from users where uid = ? ", (int(follower),))
        follower_info = c.fetchall()[0]
        if name != follower_info[1]:
            used_name = follower_info[2].split(',') if follower_info[2] else []
            used_name.append(follower_info[1])
            c.execute(f"update users set (name,used_name,still_follower) = (?,?,?) where uid = {int(follower)}",
                        (name,",".join(used_name),0))
        else:
            c.execute("update users set still_follower = 0 where uid = ? ", int(follower))
        unfollower_name.append(name)
    return ",".join(unfollower_name)


def handle_raw_follower(c, follower_raw, new_follower):
    follower_name = []
    for follower in follower_raw:
        if str(follower[0]) in new_follower:
            c.execute("insert into users (uid, name, used_name, still_follower) values (?,?,?,?)", (follower[0],follower[1],'',1))
            follower_name.append(follower[1])
        else:
            c.execute("select * from users where uid = ?", (follower[0],))
            follower_info = c.fetchall()[0]
            if follower_info[1] != follower[1]:
                used_name = follower_info[2].split(',')
                used_name.append(follower[1])
                used_name = ",".join(used_name)
                c.execute("update users set (name, used_name) = (?,?) where uid = ?", (follower[1], used_name, follower[0]))

    return ",".join(follower_name)


def write_into_db(c, followers, new_follow, new_unfollow, num) -> None:
    followers_id = ",".join(followers)
    new_followers_id = ",".join(new_follow)
    new_unfollowers_id = ",".join(new_unfollow)
    c.execute("insert into follower (followers_id, new_followers_id, new_unfollowers_id, num_followers) values (?,?,?,?)",
                (followers_id, new_followers_id, new_unfollowers_id, num))


def send_mail(new_unfollow_name):
    import yagmail
    username = os.getenv('GMAIL_USERNAME')
    password = os.getenv('GMAIL_PASSWORD')
    receiver = os.getenv('ICLOUD_USERNAME')
    yag = yagmail.SMTP(username, password)
    contents = [f'你今天被这些人取关了: {new_unfollow_name}','点击b站链接查看详细情况 https://www.bilibili.com']
    yag.send(receiver, 'b站粉丝变动自动推送', contents)  


if __name__ == "__main__":
    try:
        # resource_dir = os.getcwd()
        with open('bin/resource/xc_info.json') as f:
            xc_info = ujson.load(f)
        uid = xc_info.get('uid')
        sessdata = xc_info.get('sessdata')
        verify = bi.Verify(sessdata=sessdata)
        
        resp = bi.user.get_followers(uid=uid, verify=verify)
        num = len(resp)

        conn = sqlite3.connect('bin/resource/followers.db')
        c = conn.cursor()

        msg = ""

        followers_raw, followers = followers_filter(resp)
        old_followers = get_old_followers(c)
        new_follow, new_unfollow = diff_followers(followers, old_followers)

        if new_unfollow:
            new_unfollow_name = handle_unfollower(c, new_unfollow)
            msg += f'今日取关: {new_unfollow_name}'
            try:
                send_mail(new_unfollow_name)
            except Exception as e:
                logger.error('Send email failed', exc_info=e)

        new_follow_name = handle_raw_follower(c, followers_raw, new_follow)
        if new_follow:
            msg += f'今日粉丝: {new_follow_name}\n'

        if new_follow or new_unfollow:
            write_into_db(c, followers, new_follow, new_unfollow, num)
            logger.info('Cronjob success, check your email')

            notify(msg, title= 'b站粉丝变动', appIcon="bin/resource/bilibili.png", open='https://www.bilibili.com')

        else:
            logger.info('Cronjob success, nothing has changed')

        conn.commit()
        conn.close()
    
    except Exception as e:
        logger.error('Cronjob failed', exc_info=e)
