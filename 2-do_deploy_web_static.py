#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy
"""
from fabric.api import *
from os.path import exists
env.hosts = ['52.201.211.42', '54.89.194.2']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        filename = archive_path.split('/')[-1]
        folder_name = "/data/web_static/releases/" + filename.split('.')[0]

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))
        return True
    except Exception:
        return False
