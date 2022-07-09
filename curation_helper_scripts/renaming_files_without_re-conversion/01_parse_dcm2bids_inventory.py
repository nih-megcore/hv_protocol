import argparse
import os
import re
import subprocess
from pathlib import Path

import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description="Creates text files with each series description as the filename. "
                                                 "These files contain a list of scan names associated with "
                                                 "the series description.")

    parser.add_argument("-i", "--input-dir", type=Path, action='store', dest='inputdir', metavar='INPUT',
                        help="Path to input directory with current filenames.")
    parser.add_argument("-o", "--output-dir", type=Path, action='store', dest='outdir', metavar='OUTPUT',
                        help="Path to directory where outputs of this script will be stored.")
    parser.add_argument("-s", "--series-desc-list", type=Path, action='store', dest='series_desc_file', metavar='FILE',
                        help="Path to series description list file.")

    args = parser.parse_args()

    # converting relative to absolute paths
    inputdir = Path(os.path.abspath(args.inputdir))
    outdir = Path(os.path.abspath(args.outdir))
    series_desc_file = Path(os.path.abspath(args.series_desc_file))

    return inputdir, outdir, series_desc_file


def run_shell_cmd(cmdstr):
    pipe = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, encoding='utf8', shell=True)
    return pipe.stdout


def main():
    inputdir, outdir, series_desc_file = parse_arguments()
    data = Path(os.path.abspath('data/series_description_groups'))
    if not data.exists():
        data.mkdir(parents=True)

    desc_list = pd.read_csv(series_desc_file, sep='\n', header=None)[0].to_list()

    cmds_list = []
    for description in desc_list:
        # description is modified to exclude parenthesis and joined by '_' char
        # eg "Axial rsfMRI (Eyes Open)" becomes "Axial_rsfMRI_Eyes_Open"
        modified_description = re.sub(r"[\([{})\]]", "", description)
        modified_description = '_'.join(modified_description.split())

        # writes out bids files having a particular series description to a text file with series description as its
        # filename
        outfile = data.joinpath(modified_description + '.txt')
        bash_cmd = f"for i in `find {inputdir} -name '*.json'`; do grep -wH \"\\\"SeriesDescription\\\": \\\"{description}\\\"\" $i; done | sed 's|.json:    \"SeriesDescription\": \"{description}\",||g' > {outfile}"
        cmds_list.append(bash_cmd)
        print(bash_cmd + '\n')

    with open(outdir.joinpath('separate_out_filenames_based_on_series_descriptions.sh'), 'w') as f:
        for cmd in cmds_list:
            f.write(cmd + '\n')

    return None


if __name__ == "__main__":
    main()
