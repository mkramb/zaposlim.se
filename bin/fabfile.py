from fabric.api import local, env, cd, lcd, run, put, hosts, sudo

import time
import os

# enviroment
env.root = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')
env.release = 'master-%s' % time.strftime('%d%m%Y')
env.shell = '/bin/bash -li -c'

# remote
env.user = 'webapp'
env.password = 'webapp'
env.path = '/home/webapp'

@hosts('zaposlim-web')
def go_offline():
    with cd('/var/www/'):
        sudo('mv _maintenance.html maintenance.html')

@hosts('zaposlim-web')
def go_online():
    with cd('/var/www/'):
        sudo('mv maintenance.html _maintenance.html')

@hosts('zaposlim-web')
def deploy_web():
    # backup local files
    sudo('mv %(path)s/modules/website/settings_local.py /tmp/' % env)
    sudo('mv %(path)s/modules/website/static/CACHE/ /tmp/CACHE/' % env)

    _transfer()

    # insert local files
    sudo('mv /tmp/settings_local.py %(path)s/modules/website/' % env)
    sudo('mv /tmp/CACHE/ %(path)s/modules/website/static/CACHE/' % env)

    # init permissions
    sudo('mkdir -p %(path)s/modules/website/static/CACHE/' % env)
    sudo('mkdir -p %(path)s/modules/website/media/job/' % env)
    sudo('chmod -R 755 %(path)s/ && chown -R webapp.webapp %(path)s/' % env)

    # init cache & static files
    with cd(os.path.join(os.path.abspath(env.path), 'modules/website')):
        run('export PYTHONPATH=/home/webapp/lib:/home/webapp/modules && python manage.py compress --force')
        run('export PYTHONPATH=/home/webapp/lib:/home/webapp/modules && python manage.py cache_clear')

    # change permissions
    sudo('chown -R www-data.www-data %(path)s/modules/website/static/CACHE/' % env)
    sudo('chown -R scrapyd.scrapyd %(path)s/modules/website/media/job/' % env)

    # reset gunicorn
    sudo('/etc/init.d/gunicorn stop && sleep 2')
    sudo('export LANG=en_US.UTF-8 && /etc/init.d/gunicorn start')

@hosts('zaposlim-scraper')
def deploy_scraper():
    # backup job media
    sudo('rm -rf /tmp/job/')
    sudo('mv %(path)s/modules/website/media/job/ /tmp/job/' % env)

    _transfer()

    # replace job media
    sudo('mv /tmp/job/ %(path)s/modules/website/media/job/' % env)

    # change permissions
    sudo('mkdir -p %(path)s/modules/website/static/CACHE/' % env)
    sudo('mkdir -p %(path)s/modules/website/media/job/' % env)
    sudo('chmod -R 755 %(path)s/ && chown -R webapp.webapp %(path)s/' % env)
    sudo('chown -R www-data.www-data %(path)s/modules/website/static/CACHE/' % env)

    # restart services
    sudo('export PYTHONPATH=/home/webapp/lib:/home/webapp/modules && export JAVA_HOME=/usr/lib/jvm/java-6-sun && /etc/init.d/celeryd restart')
    sudo('/etc/init.d/scrapyd stop && /etc/init.d/scrapyd start')

    # deploy new spiders version
    with cd(os.path.join(os.path.abspath(env.path), 'modules/scraper')):
        run('scrapy deploy')

    # change permissions
    sudo('chown -R scrapyd.scrapyd %(path)s/modules/website/media/job/' % env)

@hosts('zaposlim-scraper')
def run_spiders():
    with cd('bin/'):
        run('export PYTHONPATH=/home/webapp/lib:/home/webapp/modules && python run_spiders.py')

def _transfer():
    # export to archive
    with lcd(env.root):
        local('zip -r /tmp/%(release)s.zip *' % env)

    # scp to remote server
    put('/tmp/%(release)s.zip' % env, '/tmp/%(release)s.zip' % env)
    sudo('rm -rf %(path)s && mkdir -p %(path)s' % env)

    # unzip and remove zip
    sudo('unzip /tmp/%(release)s.zip -d %(path)s/' % env)
    sudo('rm -f /tmp/%(release)s.zip' % env)

    # remove local settings (which were transfered)
    sudo('rm -f %(path)s/modules/scraper/settings_local.py*' % env)
    sudo('rm -f %(path)s/modules/website/settings_local.py*' % env)

    # remove local cache and images
    sudo('rm -rf %(path)s/modules/website/static/CACHE/' % env)
    sudo('rm -rf %(path)s/modules/website/media/job/' % env)
