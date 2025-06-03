#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static folder
    """
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)
        archive_path = "versions/{}".format(archive_name)
        
        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))
        
        file_size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(archive_path, file_size))
        
        return archive_path
    except Exception:
        return None


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


def deploy():
    """
    Creates and distributes an archive to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    
    return do_deploy(archive_path)
