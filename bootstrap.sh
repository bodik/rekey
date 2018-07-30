#!/bin/sh

if [ ! -d /opt/rekey ]; then
	cd /opt
	git clone https://rsyslog.metacentrum.cz/rekey.git
else
	cd /opt/rekey
	git remote set-url origin https://rsyslog.metacentrum.cz/rekey.git
	git pull
fi

cd /opt/rekey && git remote set-url origin bodik@rsyslog.metacentrum.cz:/data/rekey.git
