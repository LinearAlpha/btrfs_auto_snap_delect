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

err_sDir= \
'''
The snapshot directory is not setted, please set snapshot directory
by using \"-d\" or \"--snap_dir\" option
'''


err_term = \
'''
Cannon reconize \"%s\", please check help to check right option
The posivle options are \"days, week, months, years\"
Please, check help by \"-h\" or \"--help\" flag'
'''




def usage():
    # Print usag of this program
    print(use)


def del_snap(d):
    # Funsiton that format and send commned to the console
    old_dir = str()
    for id in d:
        lsit_dic = d[id]
        lsit_dic.sort()
        if len(lsit_dic) > 0:
            for v in lsit_dic[1:]:
                old_dir = old_dir + ' ' + str(v[1])
        # error, I do not know this can happend
        else:
            print('I do not know how this happend')
    rtShell = subprocess.call(
        ['echo', 'btrfs', 'subvolume', 'delete', '-vc', old_dir]
        )
    # If there is an error, print error message to the console
    if rtShell != 0:
        print('Error! (Return code %s)' % (str(rtShell)))
        sys.exit(2)


def main():
    # Read options, if option is unknown, print error message to console
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hs:d:n:",
            ["help", "snap_dir", "del_term", "--num_term"]
        )
    except getopt.GetoptError as err:
        print('\n', err)
        print('To see usage, please use \"-h\" or \"--help\" flag')
        # The program exited with error
        sys.exit(2)

    # Settting for each options
    snap_dir = str()
    term = str()
    numTerm = int()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-s', '--snap_dir'):
            snap_dir = arg
        elif opt in ('-d', 'term'):
            term = arg
        elif opt in ('-n', '--num_term'):
            try: 
                numTerm = int(arg)
            except ValueError:
                print('\nThe number of term need to be int')
                sys.exit(2)


    # Check if snapshot directory is setted
    if snap_dir == str():
        print(err_sDir)
        # The program exited with error
        sys.exit(2)

    # Setting global variables
    curTime = datetime.datetime.now()
    if numTerm == 0:
        numTerm = 1
    # Setting the period time to keep snapshots
    if term == str() or term == 'months':
        term = 'months'
        snPeriod = datetime.timedelta(days=30 * numTerm)
    elif term == 'days':
        snPeriod = datetime.timedelta(days=numTerm)
    elif term == 'weeks':
        snPeriod = datetime.timedelta(weeks=numTerm)
    elif term == 'years':
        snPeriod = datetime.timedelta(days=365 * numTerm)
    else:
        # error message
        print(err_term % (term))
        # The program exited with error
        sys.exit(2)
    dictOld = dict()  # List thay holds order then snPeriod

    try:
        ls_dir = os.listdir(snap_dir)
    except:
        print('\nNo such file or directory: \'%s\'' % snap_dir)
        sys.exit(2)

    # Read the list of snapshos from directory
    for file in ls_dir:
        # check the program is runnin same directory as sanpshot
        if not os.path.isfile(file):
            data = file.split('-').pop(1).split('_').pop(0).split('.') + \
                file.split('-').pop(1).split('_').pop(1).split('.')
            data = tuple(map(int, data))
            timestamp = datetime.datetime(
                data[0], data[1], data[2], data[3], data[4], data[5]
            )

        # If there is no marching ccase exit the program
        old = curTime - timestamp
        if old >= snPeriod:
            if term == str() or term == 'months':
                id = data[0:2]
            elif term == 'days':
                id = data[0:4]
            elif term == 'weeks':
                id = data[0:3]
            elif term == 'years':
                id = data[0:1]
            else:
                pass
            if id not in dictOld:
                dictOld[id] = list()
            dictOld[id].append([timestamp, file])
    # Case for no snapshot that older then setting
    if dictOld == dict():
        print('There is no snapshot older then %d %s' % (numTerm, term))
        sys.exit()
    return dictOld


if __name__ == "__main__":
    toDelect = main()
    del_snap(toDelect)
