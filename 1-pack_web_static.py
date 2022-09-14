#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""

from fabric.operations import local
from datetime import datetime


def do_pack():
    """comment"""
    local("mkdir -p versions")
    ret = local("tar zcvf versions/web_static_{}.tgz web_static"
                .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))
    if ret.failed:
        return None
    else:
        return ret
