# ldjsub.py
#
# David Adams
# October 2022

import desc.ldjsub
import sys
import os
import datetime
import socket
import subprocess

def ldjsub(dpat,submit, check=False, dbg=0):
    myname = 'ldjsub'
    if dbg: print(f"{myname}: Dir: {dpat}")
    if os.path.exists(dpat):
       print(f"{myname}: ERROR: Directory already exists: {dpat}")
       return 1
    dnam = os.path.basename(dpat)
    labs = dnam.split('--')
    # Drop numeric version at the end.
    if len(labs) and labs[-1].isnumeric():
        labs = labs[0:-1]
    coms = []
    args = []
    for lab in labs:
        [nam, arg] = lab.split('-', 1)
        com = f"ldj-create-{nam}"
        try:
            if dbg: print(f"{myname}: Checking command {com}")
            subprocess.call([com])
            coms += [com]
            args += [arg]
        except FileNotFoundError:
            print(f"{myname}: Command not found: {com}")
            return 1
    if len(coms) == 0:
        print(f"{myname}: Invalid label: {dnam}")
        return 1
    rmdir = False
    if not os.path.exists(dpat):
        try:
            os.mkdir(dpat)
            if check: os.rmdir(dpat)
        except:
            print(f"{myname}: ERROR: Unable to create directory {dpat}")
            return 1
    os.chdir(dpat)
    for icom in range(len(coms)):
        rstat = subprocess.call([coms[icom], args[icom]])
        if rstat:
            print(f"{myname}: ERROR: Command failed: {coms[icom]} {args[icom]}")
            return 1
    if dbg: print(f"{myname}: Done.")
    if submit:
        return ldjstart(dpat)

def ldjstart(dpat):
    myname = 'ldjstart'
    if not os.path.exists(dpat):
       print(f"{myname}: ERROR: Directory not found: {dpat}")
       return 1
    fnam = 'submit'
    fpat = dpat + '/' + fnam
    fout = fpat + '.log'
    err = False
    if os.path.exists(fout):
       print(f"{myname}: ERROR: Job already run--Log exists: {fout}")
       return 1
    stdout = open(fout, 'w')
    os.chdir(dpat)
    com = ['bash', fnam]
    print(f"Submitting job {fpat}")
    subprocess.run(com, stdout=stdout, stderr=stdout)
    if not os.path.exists(fpat):
       print(f"{myname}: ERROR: Run script not found: {fpat}")
       return 1
    stdout.close()
    sepline = '-------------------------------'
    print(sepline)
    stdout = open(fout, 'r')
    for line in stdout.readlines():
        print(line, end='')
    stdout.close()
    print(sepline)

def main_ldj_create():
    dohelp = False
    check = False
    submit = False
    dpat = None
    dbg = 0
    for arg in sys.argv[1:]:
        if arg == '-h':
            dohelp = True
        elif arg == '-c':
            check = True
        elif arg == '-s':
            submit = True
        elif arg == '-v':
            dbg = 1
        elif arg[0] == '-':
            print(f"ERROR: Invalid flag: {arg}")
            return 1
        elif dpat is None:
            dpat = os.path.abspath(arg)
        else:
            print(f"{com}: Too many arguments.")
            return 1
    if dohelp:
        com = sys.argv[0]
        print(f"Usage: {com} [-c] [-s] [-v] PATH")
        print(f"  -c: Check only. Directory is not created.")
        print(f"  -s: Submit job after creation.")
        print(f"  -v: Verbose.")
        print(f"PATH is the created run directory and can be either LABEL or DIR/LABEL")
        print(f"where LABEL is a sequence of sub-labels SLAB1--SLAB2--SLAB3....")
        print(f"The run directory is populated by running commands for the form")
        print(f"  ldj-create-TYPE ARGS") 
        print(f"specified by the sub-labels with form TYPE-ARGS.")
        return 0
    return ldjsub(dpat, submit, check, dbg)

def main_ldj_start():
    dohelp = False
    check = False
    dpat = None
    for arg in sys.argv[1:]:
        if arg == '-h':
            dohelp = True
        elif dpat is None:
            dpat = os.path.abspath(arg)
        else:
            print(f"{com}: Too many arguments.")
            return 1
    if dohelp:
        com = sys.argv[0]
        print(f"Usage: {com} DIR")
        return 0
    return ldjstart(dpat)
