"""
Call this like ``python scripts/create-venv-script.py``; it will
refresh the boot.py script
"""
import os
import subprocess
import re

here = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(here)
script_name = os.path.join(base_dir, 'boot.py')

import virtualenv


def main():
    
    installer = os.path.join(here, '_installer.py') # _installer.py
    print "Using as template: %s" % installer
    EXTRA_TEXT = open(installer).read()
    
    text = virtualenv.create_bootstrap_script(EXTRA_TEXT)
    if os.path.exists(script_name):
        f = open(script_name)
        cur_text = f.read()
        f.close()
    else:
        cur_text = ''
    print 'Updating %s' % script_name
    if cur_text == text:
        print 'No update'
    else:
        print 'Script changed; updating...'
        f = open(script_name, 'w')
        f.write(text)
        f.close()

if __name__ == '__main__':
    main()
