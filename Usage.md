usage: listforge.py [-h] [-i INPUT [INPUT ...]] [-o OUTPUT]
[--min-len MIN_LEN] [--max-len MAX_LEN]
[--require-upper] [--require-lower] [--require-digit]
[--require-special]
[--no-upper] [--no-lower] [--no-digit] [--no-special]
[--match MATCH] [--exclude EXCLUDE]
[--blacklist BLACKLIST] [--whitelist WHITELIST]
[--dedupe] [--strip] [--encoding ENCODING]


Filter words from wordlists by user-defined conditions.

-i/--input : One or more input files. If omitted, reads from stdin.

-o/--output : Output file path. If omitted, writes to stdout.

--min-len / --max-len : Minimum and maximum accepted lengths.

--require-upper, --require-lower, --require-digit, --require-special : Require at least one character of that class.

--no-upper, --no-lower, --no-digit, --no-special : Disallow any characters of that class.

--match : Keep only words that fully match the given regex (Python-style). Use quotes to protect shell.

--exclude : Exclude words that fully match this regex.

--blacklist / --whitelist : Path to files containing words (one per line). Whitelist entries are always kept; blacklist entries are always dropped.

--dedupe : Remove duplicates in output (keeps first occurrence).

--strip : Strip trailing and leading whitespace from input lines (default true).

--encoding : File encoding (default utf-8).
