#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers
"""
from fabric.api import env, run, put
from os.path import exists

env.hosts = ['52.201.211.42', '54.89.194.2']


def do_deploy(archive_path, ssh_key, username):
    """
    Distributes an archive to the web servers
    """
    env.key_filename = ssh_key
    env.user = username

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
        print("New version deployed!")
        return True
    except Exception as e:
        return False
