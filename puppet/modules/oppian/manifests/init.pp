class oppian {

  package { "system-release" :
    ensure => 'latest',
  }
  
  package { "mysql": }
  package { "mysql-devel": 
    require => Package["mysql"],
  }

  class { "webapp::python": owner => "root",
                          group => "wheel",
                          src_root => "/deploy",
                          nginx_workers => 2,
                          monit_admin => "matt@oppian.com",
                          monit_interval => 30,
                          require => [Package["mysql-devel"], Package['system-release']],
  }
  
  webapp::python::instance { "oppianproj":
    domain => "oppian.com",
    django => true,
    requirements => true,
    django_syncdb => true,
    pythonpath => ["lib/django", "apps", "apps/oppianapp/utils", "lib/django-storages"],
  }
  
  $debug_django = "False"
  
  file { "/deploy/oppianproj/settings_local.py":
    ensure => file,
    content => template('oppian/settings.py.erb'),
  }

}
