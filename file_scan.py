import os
import argparse
import re
import time
import pprint

START = time.perf_counter()
PP = pprint.PrettyPrinter(indent=4)

PARSER = argparse.ArgumentParser(
    description="Lists all files in a filepath that matches a regex string")
PARSER.add_argument("filepath", type=str, help="Enter a filepath")
PARSER.add_argument("regexp", type=str, help="Enter regexp string to match")
ARGS = PARSER.parse_args()

MATCHES = []

try:
    re.compile(ARGS.regexp)
    IS_VALID = True
except re.error:
    IS_VALID = False


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
                    MATCHES.append(pathname)
        else:
            walkpath(pathname, string_to_match)


if IS_VALID:
    STOP = time.perf_counter()
    walkpath(ARGS.filepath, ARGS.regexp)
    if len(MATCHES) > 0:
        PP.pprint(MATCHES)
    else: 
        print('No Matches Found')

    print("Elapsed time during the whole program in seconds:",
          STOP - START)
else:
    print('Please Enter a valid Regular Expression')
