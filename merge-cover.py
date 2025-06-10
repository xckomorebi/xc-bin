#! /usr/bin/env python

from argparse import ArgumentParser
from collections import OrderedDict

def parse_args():
    parser = ArgumentParser(description="Merge golang coverage functions multiple lines.")
    parser.add_argument("-i", "--input", type=str, default="coverage.txt",)
    parser.add_argument("-o", "--output", type=str, default="coverage-merged.txt")
    parser.add_argument("-s", "--substitute", type=str, help="substitute certain pattern")

    return parser.parse_args()
    

def main():
    output = []
    args = parse_args()

    d = OrderedDict()
    
    with open(args.input, "r") as f:
        for line in f:
            if line.startswith("mode:"):
                output.append(line.strip())
                continue
            
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            
            func = parts[:2]
            count = int(parts[2])
            
            key = " ".join(func)
            if key not in d:
                d[key] = count
            else:
                d[key] += count
    
    for key, count in d.items():
        if args.substitute:
            key = key.replace(args.substitute, "")
        output.append(f"{key} {count}")
    with open(args.output, "w") as f:
        f.write("\n".join(output) + "\n")
            
if __name__ == "__main__":
    main()