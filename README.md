# kerberos rekeying howto



## install

`puppet apply install.pp`



## rekeying procedure

* must be run on kdc master node (kadmin local)
* operator must have valid credentials to access managed (--keytab ssh://...) and configuration management (--puppetstorage ssh://...) node

1. install rekey utility
	* `git clone https://rsyslog.metacentrum.cz/rekey.git`
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



## manual rekeying

* generate rekeying command by rekey-self.py and execute them manually
```
./rekey-self.py --keytab=/etc/krb5.keytab --principal=host/$(hostname -f)@REALMX
```


## krbtgt rollover

* users from base realm (RSYSLOG3h) can access trusting realm (RSYSLOG3m)

### MIT Kerberos
```
ank -randkey krbtgt/RSYSLOG3m@RSYSLOG3h
cpw -e des3-cbc-sha1,aes256-cts-hmac-sha1-96 -keepold -pw '' krbtgt/RSYSLOG3m@RSYSLOG3h
getprinc krbtgt/RSYSLOG3m@RSYSLOG3h
purgekeys -keepkvno X krbtgt/RSYSLOG3m@RSYSLOG3h
```

### Heimdal kerberos

note: must have kadmin prune functionality [https://github.com/bodik/heimdal/tree/feature-h7.1-prune_principal_v1]

```
ank --use-defaults --random-key krbtgt/RSYSLOG3m@RSYSLOG3h
cpw --keepold -p '' krbtgt/RSYSLOG3m@RSYSLOG3h
get krbtgt/RSYSLOG3m@RSYSLOG3h
prune krbtgt/RSYSLOG3m@RSYSLOG3h prunekvno
```
