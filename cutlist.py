#!/usr/bin/env python3
"""
wordfilter.py

A CLI wordlist/dictionary filter.

Usage examples in README.md
"""

import sys
import argparse
import re
from typing import Iterable, Optional


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Filter words from wordlists by user-defined conditions.")
    p.add_argument('-i', '--input', nargs='*', help='Input file(s). If omitted, read from stdin.')
    p.add_argument('-o', '--output', help='Output file. If omitted, write to stdout.')

    p.add_argument('--min-len', type=int, help='Minimum word length (inclusive).')
    p.add_argument('--max-len', type=int, help='Maximum word length (inclusive).')

    p.add_argument('--require-upper', action='store_true', help='Require at least one uppercase character.')
    p.add_argument('--require-lower', action='store_true', help='Require at least one lowercase character.')
    p.add_argument('--require-digit', action='store_true', help='Require at least one digit.')
    p.add_argument('--require-special', action='store_true', help='Require at least one special (non-alnum) character.')

    p.add_argument('--no-upper', action='store_true', help='Disallow any uppercase characters.')
    p.add_argument('--no-lower', action='store_true', help='Disallow any lowercase characters.')
    p.add_argument('--no-digit', action='store_true', help='Disallow any digit characters.')
    p.add_argument('--no-special', action='store_true', help='Disallow special characters (non-alnum).')

    p.add_argument('--match', help='Keep only words matching this regular expression (full match).')
    p.add_argument('--exclude', help='Exclude words matching this regular expression (full match).')

    p.add_argument('--blacklist', help='File with words (one per line) to exclude.')
    p.add_argument('--whitelist', help='File with words (one per line) to always include.')

    p.add_argument('--dedupe', action='store_true', help='Remove duplicate outputs (keeps first occurrence).')
    p.add_argument('--strip', action='store_true', default=True, help='Strip whitespace from lines (default: true).')
    p.add_argument('--encoding', default='utf-8', help='File encoding to read/write (default utf-8).')

    return p.parse_args()


def load_set_file(path: str, encoding: str = 'utf-8') -> set:
    s = set()
    try:
        with open(path, 'r', encoding=encoding, errors='ignore') as fh:
            for ln in fh:
                w = ln.rstrip('\n\r')
                if w:
                    s.add(w)
    except FileNotFoundError:
        raise
    return s


def iter_inputs(paths: Optional[list], encoding: str = 'utf-8') -> Iterable[str]:
    if not paths:
        for ln in sys.stdin:
            yield ln
        return
    for p in paths:
        with open(p, 'r', encoding=encoding, errors='ignore') as fh:
            for ln in fh:
                yield ln


def compile_re(pattern: Optional[str]):
    if not pattern:
        return None
    return re.compile(pattern)


def check_word(word: str, args, re_match, re_exclude, blacklist: set, whitelist: set) -> bool:
    # exact checks
    if whitelist and word in whitelist:
        return True
    if blacklist and word in blacklist:
        return False

    L = len(word)
    if args.min_len is not None and L < args.min_len:
        return False
    if args.max_len is not None and L > args.max_len:
        return False

    if args.require_upper and not any(c.isupper() for c in word):
        return False
    if args.require_lower and not any(c.islower() for c in word):
        return False
    if args.require_digit and not any(c.isdigit() for c in word):
        return False
    if args.require_special and not any((not c.isalnum()) for c in word):
        return False

    if args.no_upper and any(c.isupper() for c in word):
        return False
    if args.no_lower and any(c.islower() for c in word):
        return False
    if args.no_digit and any(c.isdigit() for c in word):
        return False
    if args.no_special and any((not c.isalnum()) for c in word):
        return False

    if re_match and not re_match.fullmatch(word):
        return False
    if re_exclude and re_exclude.fullmatch(word):
        return False

    return True


def main():
    args = parse_args()

    blacklist = set()
    whitelist = set()
    if args.blacklist:
        blacklist = load_set_file(args.blacklist, args.encoding)
    if args.whitelist:
        whitelist = load_set_file(args.whitelist, args.encoding)

    re_match = compile_re(args.match)
    re_exclude = compile_re(args.exclude)

    seen = set() if args.dedupe else None

    out_fh = open(args.output, 'w', encoding=args.encoding) if args.output else None

    try:
        for raw in iter_inputs(args.input, encoding=args.encoding):
            ln = raw.rstrip('\n\r') if args.strip else raw
            if not ln:
                continue
            word = ln
            # basic normalization: we keep original casing; allow whitelist exact matches
            if check_word(word, args, re_match, re_exclude, blacklist, whitelist):
                if seen is not None:
                    if word in seen:
                        continue
                    seen.add(word)
                if out_fh:
                    out_fh.write(word + '\n')
                else:
                    sys.stdout.write(word + '\n')
    finally:
        if out_fh:
            out_fh.close()


if __name__ == '__main__':
    main()
