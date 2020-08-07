import os
import argparse
import re
import time
import pprint

start = time.perf_counter()
pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(
    description="Lists all files in a filepath that matches a regex string")
parser.add_argument("filepath", type=str, help="Enter a filepath")
parser.add_argument("regexp", type=str, help="Enter regexp string to match")
args = parser.parse_args()

matches = []

try:
    re.compile(args.regexp)
    is_valid = True
except re.error:
    is_valid = False


def walkpath(dirname, string_to_match):
    string_to_match = re.compile(string_to_match)
    children = [f for f in os.listdir(dirname)]
    for child in children:
        pathname = os.path.join(dirname, child)
        if os.path.isfile(pathname):
            with open(pathname, 'r', encoding='unicode_escape', errors='ignore') as file:
                data = file.read()
                match = string_to_match.search(data)
                file.close()
                if match:
                    matches.append(pathname)
        else:
            walkpath(pathname, string_to_match)


if is_valid:
    stop = time.perf_counter()
    walkpath(args.filepath, args.regexp)
    pp.pprint(matches)
    print("Elapsed time during the whole program in seconds:",
        stop - start)
else:
    print('Please Enter a valid Regular Expression')
