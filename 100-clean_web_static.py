#!/usr/bin/python3
"""
 generates a .tgz archive from the contents
"""

from datetime import datetime
from fabric.api import local, put, run, env
import os.path

env.hosts = ['34.73.121.48', '34.235.116.181']


def do_clean(number=0):
    """ This function retorn type of number """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
