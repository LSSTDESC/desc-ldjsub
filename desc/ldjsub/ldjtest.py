# ldjtest.py
#
# David Adams
# October 2022

import desc.ldjsub
import datetime
import socket
import os
import stat
import sys
import subprocess

def ldjtest(sargs):
    myname = 'ldjtest'
    date = datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Z')
    print(f"{myname}: ldjsub {desc.ldjsub.version()}")
    print(f"{myname}: {date}")
    print(f"{myname}: Running on {socket.gethostname()}", flush=True)
    if len(sargs):
        for sarg in sargs.split('++'):
            print(f"{myname}: >>>>>>>> {sarg}", flush=True)
            try:
                subprocess.run(sarg.split('+'))
            except FileNotFoundError:
                print(f"{myname}: ERRROR: File not found: {sarg}", flush=True)
                return 1
    print(f"{myname}: stderr date: {date}", file=sys.stderr, flush=True)

def main_ldjtest():
    args = ''
    if len(sys.argv) > 1:
        args = sys.argv[1]
    ldjtest(args)

def main_create_ldjtest():
    com = 'ldj-test'
    args = ''
    if len(sys.argv) > 1:
        args = sys.argv[1]
    if args == '-h':
        print(f"Usage: {sys.argv[0]} COM1++COM2...")
        print(f"       Use '+' to denote spaces in COMi")
        return(0)
    fnam = 'submit'
    fil = open(fnam, 'w')
    fil.write(f"{com} {args}\n")
    fil.close()
    fst = os.stat(fnam)
    os.chmod(fnam, fst.st_mode | stat.S_IEXEC)
