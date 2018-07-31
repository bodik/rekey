# kerberos rekeying howto



## install

`puppet apply install.pp`



## rekeying procedure

* must be run on kdc master node (kadmin local)
* operator must have valid credentials to access managed (--keytab ssh://...) and configuration management (--puppetstorage ssh://...) node

1. install rekey utility
	* git clone rsyslog3.git repo
	* create `kadmin-rekey.conf` = `/etc/heimdal-kdc/kdc.conf` + `/etc/krb5.conf` + edit `[kadmin] default_keys`
	* test rekeying local test keytab (see `tests/rekey_service_heimdal.sh`)


2. rekey principals
	* list principals `kadmin-list-heimdal.sh REALM | grep des-`
	* rekey principal `rekey.py --keytab X --principal Y --puppetstorage Z`, eg.
```
export FQDN="xxx"; ./rekey.py --keytab ssh://{FQDN}/etc/krb5.keytab --principal host/${FQDN} --puppetstorage ssh://puppetmaster/path/krb5.keytab.${FQDN}
```


3. wait for max renew time for existing service tickets to expire


4. cleanup keytab `rekey.py --keytab X --principal Y --puppetstorage Z --action cleanupkeytab`
```
export FQDN="xxx"; ./rekey.py --keytab ssh://${FQDN}/etc/krb5.keytab --principal host/${FQDN} --puppetstorage ssh://puppetmaster/path/krb5.keytab.${FQDN} --action cleanupkeytab
```


5. cleanup keytab backups (`*.rekeybackup.*`)
