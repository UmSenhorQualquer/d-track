#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pip, os
from subprocess import call

SUBMODULES_FOLDERS = [
    'logging-bootstrap-lib',
    'pysettings-lib',
    'pyforms-lib',
    'pyOSC-lib',
    'py3dengine-lib',
    '.'
]



def install():
    for submodule in SUBMODULES_FOLDERS:
        pip.main(['install', '--upgrade', os.path.join(submodule,'.')])

def check_submodules():
    for submodule in SUBMODULES_FOLDERS:
        if not os.path.exists(os.path.join(submodule,'setup.py')):
            call(["git", "submodule", "update", "--init", "--recursive"])
            break



if __name__=='__main__': 
    check_submodules()
    install()