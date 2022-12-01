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

    add_crawl_subparser(subparser)
    add_page_rank_subparser(subparser)
    add_words_dict_subparser(subparser)
    add_search_subparser(subparser)

    args = parser.parse_args()
    if args.command == 'crawl':
        moogle_logic.crawl(args.base_url, args.index_file, args.out_file)
    elif args.command == 'page_rank':
        moogle_logic.page_rank(args.iterations, args.dict_file, args.out_file)
    elif args.command == 'words_dict':
        moogle_logic.words_dict(args.base_url, args.index_file, args.out_file)
    elif args.command == 'search':
        moogle_logic.search(args.query, args.ranking_dict_file, args.words_dict_file, args.max_results)


def add_crawl_subparser(subparser):
    crawl = subparser.add_parser('crawl')
    crawl.add_argument('base_url', type=str)
    crawl.add_argument('index_file', type=str)
    crawl.add_argument('out_file', type=str)


def add_page_rank_subparser(subparser):
    page_rank = subparser.add_parser('page_rank')
    page_rank.add_argument('iterations', type=int)
    page_rank.add_argument('dict_file', type=str)
    page_rank.add_argument('out_file', type=str)


def add_words_dict_subparser(subparser):
    words_dict = subparser.add_parser('words_dict')
    words_dict.add_argument('base_url', type=str)
    words_dict.add_argument('index_file', type=str)
    words_dict.add_argument('out_file', type=str)


def add_search_subparser(subparser):
    words_dict = subparser.add_parser('search')
    words_dict.add_argument('query', type=str, nargs='+')
    words_dict.add_argument('ranking_dict_file', type=str)
    words_dict.add_argument('words_dict_file', type=str)
    words_dict.add_argument('max_results', type=int)


if __name__ == '__main__':
    parse_input()
