#!/usr/bin/python3
"""This script creates and distributes an archive to web servers."""

import os.path
import time
from fabric.api import local, put, run
from fabric.operations import env

env.hosts = ['54.237.3.143', '100.25.31.99']


def do_pack():
    """Generate a .tgz archive from the web_static folder."""
    try:
        local("mkdir -p versions")
        file_name = "web_static_" + time.strftime("%Y%m%d%H%M%S") + ".tgz"
        local("tar -cvzf versions/{} web_static/".format(file_name))
        return "versions/{}".format(file_name)
    except Exception:
        return None

def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    if not os.path.isfile(archive_path):
       return False

    try:
        file_name = archive_path.split("/")[-1]
        folder = "/data/web_static/releases/" + file_name.split(".")[0]
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(folder))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(folder, folder))
        run("rm -rf {}/web_static".format(folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder))
        print("Deployment done")
        return True
    except Exception:
        return False


                                                                                                                     def deploy():
                                                                                                                         """Create and distribute an archive to web servers."""
    try:
        path = do_pack()
        if not path:
           return False
        return do_deploy(path)
    except Exception:
        return False
