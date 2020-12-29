#! /usr/bin/env python
import os
import json
import argparse

import requests
from get_token import get_token


def main():
    if args.file:
        file_path = args.dsl
        with open(file_path) as f:
            data = json.load(f)
    else:
        dsl = args.dsl
        data = json.loads(dsl)

    token = get_token('analysisbase')

    headers = {
        "Authorization": token,
        "X-Caller": "bytefinder"
    }
    parse_2_sql_url = "https://rangers.bytedance.net/staging/bear/api/parse2sql"
    resp = requests.post(parse_2_sql_url, json=data, headers=headers)
    ret = resp.json()

    if args.out:
        filename = os.path.splitext(args.out)[0] + '.json'
        with open(filename, 'w') as f:
            f.write(json.dumps(ret))
    else:
        print(ret)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dsl", type=str, help="Enter dsl content you want to convert to sql")
    parser.add_argument("-f", "--file", action="store_true", help="Read from a file instead of stdin")
    parser.add_argument("-o", "--out", help="Name of the Output file")
    args = parser.parse_args()

    main()
