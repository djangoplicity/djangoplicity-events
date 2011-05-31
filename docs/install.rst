Install app
===========

Option 1 (follow development):
 * Edit your projects bootstrap_settings.py in the project root. Add a line to the ``vcs_projects`` setting::
    
    ( 'djangoplicity-events', 'hg+https://eso_readonly:pg11opc@bitbucket.org/eso/djangoplicity-kiosk',),

 * Run ``make.bootstrap`` in project root.
 * Run ``fac loc deploy`` in project root.

 
Option 2 (follow specific versions):
 
 * Add djangoplicity-events==<ver> to the projects requirements.txt in your project root.
 * Run ``fac loc deploy`` in project root.
 

After following either option 1 or 2 you must also do the following common changes:

 * In your projects settings.py file djangoplicity.events to INSTALLED_APPS::

 * In your projects main admin.py file add::

    from django.contrib import admin
    from djangoplicity.contrib.admin.discover import autoregister
    
    import djangoplicity.events.admin
	autoregister( admin.site, djangoplicity.events.admin )

  * Run manage.py migrate events