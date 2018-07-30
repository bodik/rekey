package { "krb5-gss-samples": ensure => installed }
file { "/etc/heimdal-kdc/kadmin-weakcrypto.conf":
        content => template("${module_name}/etc/heimdal-kdc/kadmin-weakcrypto.conf.erb"),
        owner => root, group => "root", mode => "0644",
}
file { "/etc/heimdal-kdc/kadmin-rekey.conf":
        content => template("${module_name}/etc/heimdal-kdc/kadmin-rekey.conf.erb"),
        owner => root, group => "root", mode => "0644",
}
