# standalone install manifest

package { "krb5-gss-samples": ensure => installed }

#not sure about install_dir so cann't use created=>
exec { "makeconfig.py kadmin-weakcrypto.conf":
	command => "/usr/bin/python3 makeconfig.py --value 'des-cbc-crc:pw-salt des-cbc-md4:pw-salt des-cbc-md5:pw-salt' --output kadmin-weakcrypto.conf",
	unless => "/usr/bin/test -f kadmin-weakcrypto.conf"
}
exec { "makeconfig.py kadmin-rekey.conf":
	command => "/usr/bin/python3 makeconfig.py --value 'des3-cbc-sha1:pw-salt aes256-cts-hmac-sha1-96:pw-salt' --output kadmin-rekey.conf",
	unless => "/usr/bin/test -f kadmin-rekey.conf"
}
