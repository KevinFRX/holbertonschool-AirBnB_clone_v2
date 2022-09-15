#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from fabric.operations import local
from datetime import datetime
import os
from fabric.api import put, get, run


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
        ret = False

    filename = path.replace(".tgz", "").replace("versions/", "")
    uncompress = run('mkdir -p /data/web_static/releases/' + filename + '/')
    if uncompress.failed:
        ret = False

    unpack = run('tar -zfx /tmp/' + filename + '.tgz' +
                 ' -C /data/web_static/releases/' + filename + '/')
    if unpack.failed:
        ret = False
    
    cleanfile = run('rm /tmp/' + filename + '.tgz')
    if cleanfile.failed:
        ret = False

    move = run('cp -R /data/web_static/releases/' + filename +
               '/web_static/* /data/web_static/releases/' + filename +
               '/')
    if move.failed:
        ret = False

    delete_arch = run('rm -rf /data/web_static/releases/' + filename +
                 '/web_static')
    if delete_arch.failed:
        ret = False

    cleanfolder = run('rm -rf /data/web_static/releases/' + filename +
                      '/web_static')
    if cleanfolder.failed:
        ret = False

    delete_sym = run('rm -rf /data/web_static/current')
    if delete_sym.failed:
        ret = False

    new_sym = run('ln -sf /data/web_static/releases/' + filename +
                    '/' + ' /data/web_static/current')
    if new_sym.failed:
        ret = False

    return ret
