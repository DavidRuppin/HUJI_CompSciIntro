#####################################################
# FILE : moogle.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs ex6 2022-2023
# PAGES I USED: https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3
#####################################################
import argparse

import moogle_logic


def parse_input():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    crawl = subparser.add_parser('crawl')
    crawl.add_argument('base_url', type=str)
    crawl.add_argument('index_file', type=str)
    crawl.add_argument('out_file', type=str)

    args = parser.parse_args()
    if args.command == 'crawl':
        moogle_logic.crawl(args.base_url, args.index_file, args.out_file)


if __name__ == '__main__':
    parse_input()
