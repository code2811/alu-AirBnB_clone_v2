#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False
    
    try:
        archive_filename = archive_path.split('/')[-1]
        archive_name = archive_filename.split('.')[0]
        
        put(archive_path, '/tmp/')
        
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_name))
        
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_filename, archive_name))
        
        run('rm /tmp/{}'.format(archive_filename))
        
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(
            archive_name, archive_name))
        
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_name))
        
        run('rm -rf /data/web_static/current')
        
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_name))
        
        print("New version deployed!")
        return True
    except Exception:
        return False
