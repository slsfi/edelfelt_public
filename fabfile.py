# -*- coding: utf-8 -*-
"""
Set application deployment and system administration task scripts here
"""
STAGING = 'user@server'

PRODUCTION = 'user@server'

import logging

logging.basicConfig()
logging.getLogger('ssh.transport').setLevel(logging.ERROR)

from fabric.api import *

app_dir = '/var/sites/..'

VIRTUAlENV_PYTHON = '/home/webapp/..'


@task
def staging():
    env.hosts = [STAGING]


@task
def production():
    env.hosts = [PRODUCTION]


def venv_python(cmd):
    run(VIRTUAlENV_PYTHON + ' ' + cmd)


@task
def deploy():
    #First make sure that github is up to date
    local("git pull")
    local("git push origin master")

    with cd(app_dir):
        run('git pull')
        venv_python('manage.py collectstatic -v0 --noinput')
        venv_python('manage.py clear_cache')
        migrate()
        print "Server updated - reloading WSGI"
        run('touch Edelfelt/wsgi.py')


def migrate():
    with cd(app_dir):
        venv_python('manage.py migrate -v0 --noinput')