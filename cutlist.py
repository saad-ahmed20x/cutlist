#!/usr/bin/env python3




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