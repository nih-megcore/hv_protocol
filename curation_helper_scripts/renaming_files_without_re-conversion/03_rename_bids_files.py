import argparse
import subprocess
from pathlib import Path

import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description="Does something worth doing.")

    parser.add_argument("--input_dir", type=Path, action='store', dest='inputdir', help="Path to input directory.")
    parser.add_argument("--output_dir", type=Path, action='store', dest='outdir', help="Path to output directory.")
    parser.add_argument("--mapping_file", type=Path, action='store', dest='mapping_file',
                        help="Path to mapping file.")
    args = parser.parse_args()
    return args.inputdir, args.outdir, args.mapping_file


def run_shell_cmd(cmdstr):
    pipe = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, encoding='utf8', shell=True)

    print(pipe.stdout)
    while True:
        output = pipe.stdout.readline()
        if output.strip():
            print(output.strip())
        else:
            pass
        return_code = pipe.poll()
        if return_code is not None:
            if return_code != 0:
                print(f"ERROR: RETURN CODE {return_code} MESSAGE: {pipe.stdout}")
                print(f"ERROR: {cmdstr} failed.")
                break
            else:
                print(f"{cmdstr} was successful.")
                break


def main():
    inputdir, outdir, mapping_file = parse_arguments()

    if not outdir.exists():
        outdir.mkdir(parents=True)

    # copy over input directory contents to output directory
    run_shell_cmd(f"rsync -avP {inputdir}/ {outdir}/ ;")

    # load mapping file
    old_to_new_map_df = pd.read_csv(mapping_file)

    for idx, value in old_to_new_map_df['current_bids_filename'].items():
        old_filepath = outdir.joinpath(value)
        new_filepath = outdir.joinpath(old_to_new_map_df.at[idx, 'revised_bids_filename'])
        run_shell_cmd(f"mv {old_filepath} {new_filepath}")


if __name__ == "__main__":
    main()
