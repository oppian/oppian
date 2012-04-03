class oppian {

  $project = "oppianproj"
  $debug_django = "True"

  class { "webapp::python": owner => "root",
                          group => "wheel",
                          src_root => "/deploy",
                          nginx_workers => 2,
                          monit_admin => "matt@oppian.com",
                          monit_interval => 30,
  }
  
  webapp::python::instance { $project:
    domain => "oppian.com",
    django => true,
    requirements => true,
    django_syncdb => true,
    pythonpath => ["lib/django", "apps", "apps/oppianapp/utils", "lib/django-storages"],
  }
  
  file { "/deploy/$project/settings_local.py":
    ensure => file,
    content => template('oppian/settings.py.erb'),
  }

}
