import os
import sys
from DelSanp import DelSnap


def ch_user() -> None:
    if os.geteuid() != 0:
        print('\n\tThis script/program must run as root (sudo).\n')
        sys.exit(2)


if __name__ == "__main__":
    ch_user()
    DelSnap().del_snap()
