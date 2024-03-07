#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['52.201.211.42', '54.89.194.2']


def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web servers
        put(archive_path, '/tmp/')

        # Get the filename without extension
        file_name = archive_path.split('/')[-1].split('.')[0]

        # Create the directory to uncompress the archive
        run('mkdir -p /data/web_static/releases/{}/'.format(file_name))

        # Uncompress the archive
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(file_name, file_name))

        # Remove the archive from the web server
        run('rm /tmp/{}.tgz'.format(file_name))

        # Move the uncompressed files to proper location
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(file_name, file_name))

        # Remove the empty web_static directory
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(file_name))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(file_name))

        return True
    except Exception:
        return False
