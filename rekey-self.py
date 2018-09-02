#!/usr/bin/env python3
"""self initiated krb key rekeyer"""

import argparse
import logging
import random
import re
import shlex
import subprocess
import sys

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')


ENCTYPES = ["des3-cbc-sha1", "aes256-cts-hmac-sha1-96"]
CHOICES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$^&*()+/?,."
PASSWORD_LENGTH = 200


def main():
	"""main"""

	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", action="store_true", help="print debug messages")
	parser.add_argument("--keytab", default="/etc/krb5.keytab")
	parser.add_argument("--principal", required=True)
	args = parser.parse_args()

	if args.debug:
		logger.setLevel(logging.DEBUG)
	try:
		realm = args.principal.split("@")[1]
	except Exception:
		raise RuntimeError("principal must be fully canonicalized") from None
	if subprocess.check_output(shlex.split("ktutil --version"), stderr=subprocess.STDOUT).decode("UTF-8").find("Heimdal") == -1:
		raise RuntimeError("heimdal krb tools not found")


	# get current principal's kvno
	keytab_listing = subprocess.check_output(shlex.split("ktutil --verbose --keytab=%s list" % args.keytab)).decode("UTF-8")
	keytab_kvno = -1
	for line in keytab_listing.splitlines():
		match = re.match(r"\s*(?P<kvno>\d+)\s+(?P<enctype>\S+)\s+(?P<principal>\S+)\s+(?P<date>\S+)\s*", line.strip())
		if match and (match.group("principal") == args.principal) and (int(match.group("kvno")) > keytab_kvno):
			keytab_kvno = int(match.group("kvno"))
	if keytab_kvno < 1:
		raise RuntimeError("cannot detect current kvno from keytab")
	keytab_kvno_new = keytab_kvno+1


	# generate new key
	logger.info("PHASE1 execute on service -- generate new keys for service")
	print("export HISTFILE=/dev/null")
	password = "".join([random.SystemRandom().choice(CHOICES) for _ in range(PASSWORD_LENGTH)])
	for enctype in ENCTYPES:
		print("ktutil --keytab=%s add --principal=%s --kvno=%s --enctype=%s --password='%s'" % \
			(args.keytab, args.principal, keytab_kvno_new, enctype, password))


	# update kdb
	print()
	logger.info("PHASE2 execute on master kdc -- put keys to kdb")
	print("export HISTFILE=/dev/null")
	print("kadmin.heimdal --local --realm=%s cpw --password='%s' %s" % (realm, password, args.principal))


	# flush old keys
	print()
	logger.info("PHASE3 execute on service -- remove old keys from service keytab")
	keytab_listing = subprocess.check_output(shlex.split("ktutil --verbose --keytab=%s list" % args.keytab)).decode("UTF-8")
	for line in keytab_listing.splitlines():
		match = re.match(r"\s*(?P<kvno>\d+)\s+(?P<enctype>\S+)\s+(?P<principal>\S+)\s+(?P<date>\S+)\s*", line.strip())
		if match and (match.group("principal") == args.principal) and (int(match.group("kvno")) < keytab_kvno_new):
			print("ktutil --keytab=%s remove --principal=%s --kvno=%s --enctype=%s" % \
				(args.keytab, args.principal, int(match.group("kvno")), match.group("enctype")))


if __name__ == "__main__":
	sys.exit(main())
