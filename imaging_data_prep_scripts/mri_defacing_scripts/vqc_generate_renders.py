import argparse
import subprocess
from os import fspath
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-in', action='store', type=Path,
                        dest='inputdir', help='Path to input directory.')
    parser.add_argument('-rotations', action='store', type=str,
                        dest='rots', help='Path to text file with rotations.')
    parser.add_argument('-vqc_ids', action='store', type=Path,
                        dest='idlist', help='Path to visualqc id_list file.')

    return parser.parse_args()


def run_command(cmdstr):
    p = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         universal_newlines=True, encoding='utf8', shell=True)
    return p.stdout.readline().strip()


def main():
    args = get_args()

    # processing rotations list
    f1 = open(args.rots, 'r')
    rotations = [list(line.strip('\n').split(',')) for line in f1.readlines()]

    # processing idlist
    f2 = open(args.idlist, 'r')
    workdirs = [line.rstrip() for line in f2.readlines()]

    for workdir in workdirs:
        scan = args.inputdir.joinpath(workdir, 'tmp.99.result.deface_iso_1mm.nii.gz')
        subj_cmds = []
        print(fspath(scan).split('/')[6])
        for idx, rot in enumerate(rotations):
            yaw, pitch, roll = rot[0], rot[1], rot[2]
            outfile = scan.parent.joinpath(scan.name.split('.nii.gz')[0] + '_render_' + str(idx) + '.png')
            cmd = f"fsleyes render --scene 3d -rot {yaw} {pitch} {roll} --outfile {outfile} {scan} -dr 20 250 -in spline -bf 0.3 -r 100 -ns 500"
            subj_cmds.append(cmd)
        print(run_command('; '.join(subj_cmds)))
        print('********************************************************')


if __name__ == "__main__":
    main()
