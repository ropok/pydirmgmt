'''
for effectiveness process, run this on the daily-count-handnphone directory
'''

import os
import shutil
import argparse

class Main():
    def __init__(self):
        super(Main, self)
    
    def getVTName(self, path):
        for root, dirs, files in os.walk(path):
            for dire in dirs:
                # add special for directory name
                if dire[-3:].isnumeric() and len(dire) < 7:
                    vt_name.append(dire)
        vt_name = sorted(list(set(vt_name)))
        return vt_name

    def wavOut(self, vt_name, path):
        for vt in vt_name:
            print("processing", vt)
            path_vt = os.path.join(path, vt)
            for root, dirs, files in os.walk(path_vt):
                for file in files:
                    if file[-4:] == '.wav':
                        shutil.move(os.path.join(root, filename), os.path.join(path_vt, filename))
                        print("moved", filename)
    
    def delDupe(self, vt_name, path_src, path_dest):
        # move duplicate files into other folder (not counted on qc)
        for vt in vt_name:
            print("processing", vt)
            path_vt = os.path.join(path_src, vt)
            path_dupe = os.path.join(path_dest, vt)
            if os.path.exists(path_dupe):
                pass
            else:
                os.makedirs(path_dupe)
                print("mkdir", path_dupe)
            for root, dirs, files in os.walk(path_vt):
                for file in files:
                    if file[-5:] == ').wav':
                        shutil.move(os.path.join(root, file), os.path.join(path_dupe, file))
                        print("moved", vt, file)


# handler args
def parse_arguments():
    parser = argparse.ArgumentParser(description="python directory management")

    tasks = parser.add_subparsers(
        title="subcommands", description="available tasks",
        dest="task", metavar="")

    moveWAV = tasks.add_parser("movewav", help="[moveWAV] - pindah .wav ke folder utama")
    moveWAV.add_argument("-i", "--input", required=True, help="Nama Direktori")

    delDUPE = tasks.add_parser("deldupe", help="[delDUPE] - pindah file duplikasi")
    delDUPE.add_argument("-i", "--input", required=True, help="Nama Direktori")
    delDUPE.add_argument("-o", "--output", required=True, help="Direktori duplikasi")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    main = Main()

    # pindah .wav ke folder utama
    if args.task == "movewav":
        vt_name = main.getVTName(args.input)
        main.wavOut(vt_name, args.input)

    # hilangin duplikasi
    if args.task = "deldupe":
        vt_name = main.getVTName(args.input)
        main.delDupe(vt_name, args.input, args.output)