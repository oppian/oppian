class oppian {

  $project = "oppianproj"

  class { "webapp::python": owner => "root",
                          group => "wheel",
                          src_root => "/deploy",
                          nginx_workers => 1,
                          monit_admin => $cfn_adminemail,
                          monit_interval => 30,
  }
  
  if $cfn_hostname2 {
  	$aliases = [$cfn_hostname2]
  }
  else {
  	$aliases = []
  }

  webapp::python::instance { $project:
    workers => inline_template("<%= (processorcount.to_i * 2 + 1) -%>"),
    listen_port => 8080,
    domain => $cfn_hostname,
    aliases => $aliases,
    django => true,
    requirements => true,
    django_syncdb => true,
    mediaroot => "/deploy/$project/media/",
    mediaprefix => "/m/",
    pythonpath => ["lib/django", "apps", "apps/oppianapp/utils", "lib/django-storages"],
    default_vhost => true,
  }

  file { "/deploy/$project/settings_local.py":
    ensure => file,
    content => template('oppian/settings.py.erb'),
  }
  
  file { "/deploy/$project/media/admin":
  	ensure => link,
  	target => "/deploy/$project/lib/django/django/contrib/admin/media"
  }
  
  file { "/deploy/$project/media/favicon.ico":
  	ensure => link,
  	target => "/deploy/$project/media/images/favicon.ico"
  }

  class {'varnish':}

}
