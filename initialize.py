#!/usr/bin/env python

import sys, os
import subprocess
import urllib

def main():
    if len(sys.argv) != 2:
        print "\nUsage: %s [NAME]\nInitialize your Grok project\n" % sys.argv[0]
        return 1
    name = sys.argv[1]
    major_version = '.'.join([str(x) for x in sys.version_info[:2]])
    if major_version not in ['2.6', '2.7']:
        print "Need Python 2.6 or 2.7"
        return 1
    dirname = os.path.dirname(__file__)
    script = '''
%(python)s virtualenv.py virtualenv
./virtualenv/bin/python bootstrap.py -c grokproject.cfg
./bin/buildout -vvv -c grokproject.cfg
./bin/grokproject --run-buildout=false %(name)s
mv %(name)s/* .
rmdir %(name)s/
rm -rf bin/ develop-eggs/ parts/
git add buildout.cfg etc src setup.py
    ''' % {'name': name, 'python': sys.executable}

    for line in script.split('\n'):
        if not line.strip():
            continue
        print '+', line
        if os.system(line):
            print "+ Aborted"
            return 1


if __name__ == '__main__':
    main()
