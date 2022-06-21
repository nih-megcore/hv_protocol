from pathlib import Path
import re
import subprocess
import argparse

import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description="Creates text files with each series description as the filename. "
                                                 "These files contain a list of scan names associated with "
                                                 "the series description.")

    parser.add_argument("--input_dir", type=Path, action='store', dest='inputdir', help="Path to input directory.")
    parser.add_argument("--output_dir", type=Path, action='store', dest='outdir', help="Path to output directory.")
    parser.add_argument("--series_desc_list", type=Path, action='store', dest='outdir', help="Path to output directory.")

    return parser.parse_args()


def run_shell_cmd(cmdstr):
    pipe = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, encoding='utf8', shell=True)
    return pipe.stdout


def main():
    root = Path('/Users/arshitha/Desktop/OneDesk/Projects/17M081_June_2022')  # directory with bids formatted data and code files
    data = root.joinpath('17M081_jsons')  # bids dataset
    series_descriptions = root.joinpath('all_series_descriptions.txt')  # file with list of all unique series descriptions

    # hardcoded
    desc_with_orig = ['ADNI2 2D FLAIR', 'Anat T1w MP-RAGE 1mm (ABCD)', 'Anat T2w CUBE (ABCD)', 'Axial T2 2D FLAIR ADNI2', 'Optional - Anat T2w CUBE FLAIR','Sag_MPRAGE_T1']
    desc_with_optional = ['Sagittal 3D FLAIR']
    desc_list = pd.read_csv(series_descriptions, sep='\n', header=None)[0].to_list()

    cmds_list = []
    for description in desc_list:
        modified_description = re.sub(r"[\([{})\]]", "", description)
        outfile = '_'.join(modified_description.split())+'.txt'
        bash_cmd = f"for i in `find . -name '*.json'`; do grep -wH \"\\\"SeriesDescription\\\": \\\"{description}\\\"\" $i; done | sed 's|.json:    \"SeriesDescription\": \"{description}\",||g' > {outfile}"
        cmds_list.append(bash_cmd)
        print(bash_cmd+'\n')

    with open('17M081_jsons/separate_out_filenames_based_on_series_descriptions.sh', 'w') as f:
        for cmd in cmds_list:
            f.write(cmd+'\n')

    return None


if __name__ == "__main__":
    main()

