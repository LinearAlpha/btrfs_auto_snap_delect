import os
import subprocess
import pytz
from datetime import datetime
from CLArg import CLArg


class DelSnap:
    old_dir: list[datetime]
    current_time = datetime.now(pytz.timezone('GMT')).replace(tzinfo=None)
    # del_dir_flag: bool = True

    def __init__(self) -> None:
        self.args = CLArg()  # Read comand line argument
        self._get_old_dir()

    def _get_old_dir(self) -> list[str]:
        self.current_time = datetime.now(
            pytz.timezone('GMT')).replace(tzinfo=None)
        self.old_dir = list()
        for file in os.listdir(self.args.snap_dir):
            dir_time = datetime.strptime(file, "@GMT-%Y.%m.%d-%H.%M.%S")
            # It assumes alphametic order, so it is minningless to checking all
            # of the list variables
            if self.current_time - dir_time >= self.args.time_diff:
                self.old_dir.append(file)  # Append directory to delecte
            else:
                break

    def del_snap(self) -> None:
        # Only excute deletion command when there is a list
        # if self.del_dir_flag:
        if self.old_dir:
            dir_2_del = "btrfs subvolume delete -cv"
            for dir in self.old_dir:
                dir_2_del += " " + self.args.snap_dir + str(dir)
            mes_shell = subprocess.call(dir_2_del, shell=True)
            if mes_shell != 0:
                print('Error! (Return code %s)' % (str(mes_shell)))
        else:
            print("There is no snapshots older then %s" % self.current_time)
