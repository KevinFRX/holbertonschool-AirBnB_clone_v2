#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""
from fabric.operations import local, put, run
from datetime import datetime
import os
from fabric.api import env


env.hosts = ['54.91.233.56', '3.80.32.222']


def do_pack():
    """comment"""
    local("mkdir -p versions")
    ret = local("tar zcvf versions/web_static_{}.tgz web_static"
                .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))
    if ret.failed:
        return None
    else:
        return ret


def do_deploy(archive_path):
    """comment"""
    if not os.path.exists(archive_path):
        return False

    upload = put(archive_path, '/tmp/')
    if upload.failed:
        return False

    filename = archive_path.split('.')[0]
    filename = filename.split('/')[1]
    uncompress = run('sudo mkdir -p /data/web_static/releases/{}/'
                     .format(filename))
    if uncompress.failed:
        return False

    unpack = run('sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
                 .format(filename, filename))
    if unpack.failed:
        return False

    cleanfile = run('sudo rm -f /tmp/{}.tgz'.format(filename))
    if cleanfile.failed:
        return False

    move = run('sudo mv /data/web_static/releases/{}/web_static/* '
               '/data/web_static/releases/{}/'.format(filename, filename))
    if move.failed:
        return False

    delete_arch = run('sudo rm -rf /data/web_static/releases/{}/web_static'
                      .format(filename))
    if delete_arch.failed:
        return False

    delete_sym = run('sudo rm -rf /data/web_static/current')
    if delete_sym.failed:
        return False

    new_sym = run('sudo ln -s /data/web_static/releases/{}/ '
                  '/data/web_static/current'.format(filename))
    if new_sym.failed:
        return False

    return True
