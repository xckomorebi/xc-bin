#! /usr/bin/env python3

import os

FILENAME = "skipped_tests.txt"

def get_skip_tests() -> str:
    if not os.path.exists(FILENAME):
        return ""
    
    tests = []
    with open(FILENAME, "r") as f:
        for line in f:
            if "#" in line:
                line = line.split("#")[0]
            line = line.strip()
            if line:
                tests.append(line)

    if not tests:
        return ""

    return "-skip '" + "|".join(tests) + "'"

if __name__ == "__main__":
    print(get_skip_tests())