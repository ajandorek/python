import os
import argparse
import re
import time
import pprint
import asyncio
import aiofiles

START = time.perf_counter()
PP = pprint.PrettyPrinter(indent=4)

PARSER = argparse.ArgumentParser(
    description="Lists all files in a filepath that matches a regex string")
PARSER.add_argument("filepath", type=str, help="Enter a filepath")
PARSER.add_argument("regexp", type=str, help="Enter regexp string to match")
PARSER.add_argument("consumers", type=int, help="Enter a number of consumers", default=10)
ARGS = PARSER.parse_args()

MATCHES = []

try:
    re.compile(ARGS.regexp)
    IS_VALID = True
except re.error:
    IS_VALID = False

async def walkpath(dirname, q: asyncio.Queue):
    for root, dirs, files in os.walk(dirname):
        for file in files:
            pathname = os.path.join(root, file)
            await q.put(pathname)

async def consume(name: int, q: asyncio.Queue):
    while True:
        i = await q.get()
        if os.path.isfile(i):
            async with aiofiles.open(i, 'r', encoding='unicode_escape', errors='ignore') as file:
                    data = await file.read()
                    string_to_match = re.compile(ARGS.regexp)
                    match = string_to_match.search(data)
                    file.close()
                    if match:
                        print(f"Consumer {name} got element {i}")
                        MATCHES.append(i)
        q.task_done()

async def main(): 
    Q = asyncio.Queue()
    producers = asyncio.create_task(walkpath(ARGS.filepath, Q))
    consumers = [asyncio.create_task(consume(n, Q)) for n in range(ARGS.consumers)]
    await asyncio.gather(producers)
    await Q.join()
    for c in consumers:
        c.cancel()


if IS_VALID:
    asyncio.run(main())
    STOP = time.perf_counter()
    if len(MATCHES) > 0:
        PP.pprint(MATCHES)
    else:
        print('No Matches Found')

    print("Elapsed time during the whole program in seconds:",
          STOP - START)
else:
    print('Please Enter a valid Regular Expression')
