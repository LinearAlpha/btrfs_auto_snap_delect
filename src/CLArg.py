import sys
import getopt
import os.path
from datetime import datetime, timedelta
import pytz

USAGE = \
    '''
\nThis program assume ths sanpshot pattern as
XXX-Y.m.d_H.M.S

-h, --help:
        Print usage/help

-s, --snap_dir=<direcroty>:
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

-d, --del_term=<term>:
        Pried fo hoe long to keep snapshot
        days: Delect snapshot more then day
        weeks: Delect snapshot more then week
        months: Delect snapshot more the month
        years: Delect snapshot more then year
        Default = months

-n, --num_term=<num term>:
        Set number of period to delect
        Deafault = 1

-t, --time

'''


class CLArg:
    snap_dir: str
    del_term: str = "months"
    num_term: int = 1
    time_zone_srt: str = "GMT"
    time_zone: datetime = datetime.now(pytz.timezone(time_zone_srt))
    time_diff: datetime

    def __init__(self) -> None:
        self._read_arg()
        self._set_time()

    def _usage(self) -> None:
        """Print usage/help of this program
        """
        print(USAGE)

    def _ch_dir(self, dir) -> str | None:
        if os.path.isdir(dir):
            return dir if dir[len(dir) - 1] == '/' else dir + '/'
        else:
            print('\n\tNo such directory: \'%s\'' % dir)
            sys.exit(2)  # Exit with error

    def _read_arg(self):
        df_del_term: list[str] = ["days", "weeks", "months", "years"]
        # Check and setting CLA inputs
        try:
            opts, ext_arg = getopt.getopt(
                sys.argv[1:],
                "hs:d:n:t:",
                ["help", "snap_dir=", "del_term=", "num_term=", 'time_zone=']
            )
        except getopt.GetoptError as err:
            print('\n', err)
            self._usage()
            sys.exit(2)
        # Reading CLA
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self._usage()
                sys.exit()  # Exit without error
            elif opt in ('-d', '--snap_dir'):
                self.snap_dir = self._ch_dir(arg)
            elif opt in ('-d', '--del_term'):
                if str(arg) in df_del_term:
                    self.del_term = str(arg)
                else:
                    "valid, please check usage"
                    print(
                        "\n\t-d\\--del_term \"%s\" input is not valid, please check usage" % arg)
                    sys.exit(2)  # Exit with error
            elif opt in ('-n', '--num_term'):
                try:
                    self.num_term = int(arg)
                except:
                    print("\n\t-n\\--num_term must be integer")
                    sys.exit(2)
            elif opt in ('-t', '--time_zone'):
                if arg in pytz.all_timezones and arg == str():
                    self.time_zone_srt = arg
                    self.time_zone = datetime.now(pytz.timezone('arg'))
                else:
                    if arg != str():
                        print("\n\t-t'\'--time_zone please use string input")
                    else:
                        print(
                            "\n\t-t'\'--time_zone \"%s\" is on the time zone, please check your time zone input" % arg)
                    sys.exit(2)  # Exit with error

    def _set_time(self) -> None:
        if self.del_term == "days":
            self.time_diff = timedelta(days=self.num_term)
        elif self.del_term == "weeks":
            self.time_diff = timedelta(weeks=self.num_term)
        elif self.del_term == "months":
            self.time_diff = timedelta(days=30 * self.num_term)
        else:
            self.time_diff = timedelta(days=365 * self.num_term)

    # @snap_dir.setter
    # def snap_dir(cls, dir_tmp) -> None:
    #     cls.snap_dir = dir_tmp

    # @property
    # def snap_dir(cls) -> str:
    #     return cls.snap_dir

    # @time_zone.setter
    # def time_zone(cls, time_zone_tmp) -> None:
    #     cls.time_zone = time_zone_tmp

    # @property
    # def time_zone(cls) -> datetime:
    #     return cls.time_zone


# if __name__ == "__main__":
#     CLArg()
