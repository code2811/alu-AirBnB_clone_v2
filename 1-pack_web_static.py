#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


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
