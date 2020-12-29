#! /usr/bin/env python
import os
import enum
import argparse
import requests


class Callee(enum.Enum):
    pass


def get_token(callee = 'analysisbase'):
    url = "https://rangers.bytedance.net/byterangers/innerapi/v2/jwt"
    resp = requests.get(url, headers={"Authorization": os.getenv("BYTEFINDER_JWT_TOKEN")}, params={"callee": callee})
    token = resp.json()["data"]["jwt"]
    return token


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("callee", type=str, nargs='?', default='analysisbase')
    args = parser.parse_args()

    print(get_token(args.callee))