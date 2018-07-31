#!/usr/bin/python3

import argparse
import re
import sys


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("--value", default="des3-cbc-sha1:pw-salt", required=False)
	parser.add_argument("--output", required=False)
	return parser.parse_args()


def main():
	config = []
	config_new = []
	section = None

	args = parse_arguments()

	if args.output:
		sys.stdout = open(args.output, "w")

	for fname in ["/etc/heimdal-kdc/kdc.conf", "/etc/krb5.conf"]:
		config.append("## included %s" % fname)
		with open(fname) as ftmp:
			config += ftmp.read().splitlines()

	for line in config:
		match = re.search(r"\[(?P<section>.*)\]", line)
		if match:
			section = match.group("section")

		if section == "kadmin":
			match = re.search(r"\s+default_keys\s+=", line)
			if match:
				config_new.append("#"+line)
				continue

		config_new.append(line)

	config_new.append("## replaced configuration")
	config_new.append("[kadmin]")
	config_new.append("default_keys = %s" % args.value)

	print("\n".join(config_new))

if __name__ == "__main__":
	main()
