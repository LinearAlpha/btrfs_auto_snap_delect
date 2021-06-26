#!/usr/bin/python3
import os
import os.path
import sys
import getopt
import datetime
import subprocess

use = \
    '''
This program assume ths sanpshot pattern as
@GMT-%Y.%m.%d_%H.%M.%S
The \"@GMT\" can be anything

-h, --help:
        Print usage/help

-S, --Sync:
        Run commend \'btrfs filesystem sync\' to force a sync on filessystem
        after delect snapshots.
        For this option, it need full path of mounting point
        ex)
        If the drive is mounted on /mnt/BTRFS
        sn_del -S /mnt/BTRFS ...

-s, --snap_dir <direcroty>:
        Directory of snapshot
        ex)
        .
        └── mnt
            └── DATA
                └── .snaptho
                    └── @SN_workplace
                        └── @GMT-2021.05.30_05.30.01
                                        ⋮
                                        ⋮
        The input need to be
        /mnt/DATA_SSD/.snapshot/@SN_workplace

-d, --del_term <term>:
        Pried fo hoe long to keep snapshot
        days: Delect snapshot more then day
        weeks: Delect snapshot more then week
        months: Delect snapshot more the month
        years: Delect snapshot more then year
        Default = months

-n, --num_term:
        Set number of period to delect
        Deafault = 1
'''

err_sDir = \
    '''
The snapshot directory is not setted, please set snapshot directory
by using \"-d\" or \"--snap_dir\" option
'''


err_term = \
    '''
Cannon reconize \"%s\", please check help to check right option
The posivle options are \"days, week, months, years\"
Please, check help by \"-h\" or \"--help\" flag
'''


def usage():
    '''
    Print usage of this program
    '''
    print(use)


def checkUser():
    '''
    Check if sctip/progam is running as root user
    '''
    if not os.geteuid() == 0:
        print('\n\tThis script/program must eun as root.\n')
        sys.exit(2)


def readSysArg():
    '''
    Read system argument, and inisitlize the system options and argument
    '''
    # Sysparameter
    snap_dir = str()
    term = str()
    numTerm = int()
    sync_dir = str()
    # Read system inpur arguement
    try:
        opts, arg = getopt.getopt(
            sys.argv[1:],
            "hs:d:n:S:",
            ["help", "snap_dir", "del_term", "--num_term", "--Sync"]
        )
    except getopt.GetoptError as err:
        print('\n', err)
        print('To see usage, please use \"-h\" or \"--help\" flag')
        # The program exited with error
        sys.exit(2)
    #Set system parameter
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-s', '--snap_dir'):
            if os.path.isdir(arg) and arg == None:
                if arg[len(arg) - 1] != '/':
                    arg = arg + '/'
                snap_dir = arg
            else:
                print('\nNo such directory: \'%s\'' % arg)
                sys.exit(2)
        elif opt in ('-d', 'term'):
            term = arg
        elif opt in ('-n', '--num_term'):
            try:
                numTerm = int(arg)
                if numTerm == 0:
                    numTerm = 1
            except ValueError:
                print('\nThe number of term need to be int')
                sys.exit(2)
        elif opt in ('-S', '--Sync'):
            if (os.path.isdir(arg)):
                sync_dir = arg
            else:
                print('\nNo such directory: \'%s\'' % arg)
                sys.exit(2)
    return snap_dir, term, numTerm, sync_dir


def setPeriod(term, num):
    '''
    Set period of time to keep snapshots
    '''
    # Setting the period time to keep snapshots
    if term == str() or term == 'months':
        term = 'months'
        snPeriod = datetime.timedelta(days=30 * num)
    elif term == 'days':
        snPeriod = datetime.timedelta(days=num)
    elif term == 'weeks':
        snPeriod = datetime.timedelta(weeks=num)
    elif term == 'years':
        snPeriod = datetime.timedelta(days=365 * num)
    else:
        # error message
        print(err_term % (term))
        # The program exited with error
        sys.exit(2)
    return snPeriod


def del_snap(d, dir, mDir):
    '''
    Delect snapshots
    '''
    d.sort()
    # Funsiton that format and send commned to the console
    if len(d) > 0:
        for dir in d:
            rtShell = subprocess.call(
                ['btrfs', 'subvolume', 'delete', '-v', dir]
            )
            # If there is an error, print error message to the console
            if rtShell != 0:
                print('Error! (Return code %s)' % (str(rtShell)))
        # error, I do not know this can happend
        else:
            print('Teher is no list of directories')
    if (mDir != str()):
        subprocess.call(['btrfs', 'filesystem', 'sync', mDir])


def main():
    '''
    Main function of this program
    Initialize the lsit of directories that is order then user input.
    The period is setted by serPeriod function.
    '''
    # Get system parameter
    snap_dir, term, numTerm, sync_dir = readSysArg()
    # Set snap delete period
    snPeriod = setPeriod(term=term, num=numTerm)
    # Setting global variables
    curTime = datetime.datetime.now()
    lsOlDir = list()
    # Read the list of snapshos from directory
    for file in os.listdir(snap_dir):
        # check the program is runnin same directory as sanpshot
        if not os.path.isfile(file):
            data = file.split('-').pop(1).split('_').pop(0).split('.') + \
                file.split('-').pop(1).split('_').pop(1).split('.')
            data = tuple(map(int, data))
            timestamp = datetime.datetime(
                data[0], data[1], data[2], data[3], data[4], data[5]
            )
        # If there is no marching ccase exit the program
        if curTime - timestamp >= snPeriod:
            lsOlDir.append(file)
    # Case for no snapshot that older then setting
    if lsOlDir == list():
        print('There is no snapshot older then %d %s' % (numTerm, term))
        sys.exit()
    return lsOlDir, snap_dir, sync_dir


if __name__ == "__main__":
    checkUser()
    toDelect, snDir, syDir = main()
    del_snap(toDelect, snDir, syDir)
