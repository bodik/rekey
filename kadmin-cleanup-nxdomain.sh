#!/bin/sh

if [ -z $1 ]; then
	REALM=$(cat /etc/krb5.conf  | grep default_realm | awk '{print $3}')
else
	REALM=$1
fi



for hostprinc in $(sh kadmin-list.sh $REALM | awk '{print $1}' | grep '\.cz$'); do
	
	echo "$hostprinc" | awk -F'/' '{print $2}' | sort | uniq | xargs -I{} host -t A {} | grep NXDOMAIN 1>/dev/null 2>/dev/null
	if [ $? -eq 0 ]; then
		echo "del ${hostprinc}"
	fi
done
