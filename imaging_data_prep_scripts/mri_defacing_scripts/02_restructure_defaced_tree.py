import argparse
import subprocess
from os import fspath
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate a swarm command file to deface T1w scans for a given BIDS dataset.')

    parser.add_argument('-defaced-root', action='store', dest='output',
                        help='Path to defaced scans root directory.')

    args = parser.parse_args()
    return Path(args.output)


def run_command(cmdstr):
    p = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                         encoding='utf8', shell=True)

    stdout_capture = []
    while p.poll() is None:
        line = p.stdout.readline().strip()
        if len(line) > 0:
            stdout_capture.append(line)

    return stdout_capture


def main():
    # get command line arguments
    output = get_args()

    find_afni_workdirs = run_command(f"find {output} -name __work*")
    for workdir in find_afni_workdirs:
        workdir = Path(workdir)
        prefix = workdir.name.split('.')[1]
        to_be_deleted_files = [fspath(f) for f in list(workdir.parent.glob('*')) if not f.name.startswith('__work')]
        remove_files = f"rm -rf {' '.join(to_be_deleted_files)}"
        rename = f"mv {workdir} {workdir.parent.joinpath('workdir_' + prefix)}"
        cmd = '; '.join([remove_files, rename])
        print(f"Removing unwanted files and renaming AFNI workdirs..")
        cmd_out = run_command(cmd)
        if len(cmd_out) != 0:
            for line in cmd_out:
                print(line)


if __name__ == "__main__":
    main()
