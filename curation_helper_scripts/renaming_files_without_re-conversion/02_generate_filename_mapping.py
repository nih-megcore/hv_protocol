import argparse
import csv
import os
import re
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description="Creates text files with each series description as the filename. "
                                                 "These files contain a list of scan names associated with "
                                                 "the series description.")

    parser.add_argument("-i", "--input-dir", type=Path, action='store', dest='inputdir', metavar='INPUT',
                        help="Path to input BIDS directory with current filenames.")
    parser.add_argument("-o", "--output-dir", type=Path, action='store', dest='outdir', metavar='OUTPUT',
                        help="Path to directory where outputs of this script will be stored.")
    parser.add_argument("-s", "--series-desc-to-filenames", type=Path, action='store', dest='series_to_files',
                        metavar='FILE', help="Path to directory with text files named after unique series descriptions \
                        that has a list of filepaths associated with that particular series description.")

    args = parser.parse_args()

    # converting relative to absolute paths
    inputdir = Path(os.path.abspath(args.inputdir))
    series_to_files = Path(os.path.abspath(args.series_to_files))
    outdir = Path(os.path.abspath(args.outdir))

    return inputdir, series_to_files, outdir


def run_shell_cmd(cmdstr):
    pipe = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, encoding='utf8', shell=True)
    return pipe.stdout


def main():
    inputdir, series_to_files, outdir = parse_arguments()
    data_dir = Path(os.path.abspath('data'))
    series_filenames = list(series_to_files.glob('*.txt'))

    df_columns = ['original_series_description', 'modified_series_description', 'current_bids_filename',
                  'revised_common_identifiers', 'revised_bids_filename']
    df = pd.DataFrame(columns=df_columns)
    idx = 0
    for series_filename in series_filenames:
        desc = series_filename.name.split('.')[0]
        print(desc)
        f = open(series_filename, 'r')
        for line in f.readlines():
            filepath = Path(line.strip())
            abs_path_parts = filepath.parts

            for i, v in enumerate(abs_path_parts):
                if v == inputdir.name:
                    startidx = i + 1

            rel_filepath = '/'.join(abs_path_parts[startidx:])
            df.at[idx, 'current_bids_filename'] = rel_filepath
            df.at[idx, 'modified_series_description'] = desc
            idx += 1

    # series description to unique identifier mapping file
    series_to_identifier_df = pd.read_csv(data_dir.joinpath('series_descriptions_to_new_common_identifiers.csv'))

    grouped_df = df.groupby(by=['modified_series_description'])
    unique_series_desc = grouped_df.groups.keys()
    for series_desc in unique_series_desc:
        for idx in grouped_df.groups[series_desc]:
            curr_filename = df.at[idx, 'current_bids_filename']
            prefix = '_'.join(curr_filename.split('_')[:2])
            print(prefix)
            entities = re.split('/|_', curr_filename)

            df.at[idx, 'original_series_description'] = series_to_identifier_df.loc[series_to_identifier_df[
                                                                                        'modified_series_description'] == series_desc, 'original_series_description'].values[
                0]
            new_common_identifier = series_to_identifier_df.loc[series_to_identifier_df[
                                                                    'modified_series_description'] == series_desc, 'revised_common_identifiers'].values[
                0].strip('_')

            # replace fieldmap with magnitude for fmap scans
            if 'magnitude' in entities:
                parts = new_common_identifier.split('_')
                parts[-1] = 'magnitude'
                new_common_identifier = '_'.join(parts)

            # include run entity in new common identifier
            if 'run-01' in entities or 'run-02' in entities:
                parts = new_common_identifier.split('_')
                parts.insert(-1, entities[-2])
                new_common_identifier = '_'.join(parts)

            df.at[idx, 'revised_common_identifiers'] = new_common_identifier
            new_filename = '_'.join([prefix, new_common_identifier])
            df.at[idx, 'revised_bids_filename'] = new_filename

    new_to_old_df = df[['current_bids_filename', 'revised_bids_filename']]

    # duplicate every row exactly once. One row with nii.gz and the other with .json suffix
    with_json_new_to_old_df = pd.DataFrame(np.repeat(new_to_old_df.values, 2, axis=0), columns=new_to_old_df.columns)

    # add filename ".nii.gz" and ".json" suffix to both current and new filenames
    for idx in with_json_new_to_old_df.index:
        if idx % 2 == 0:
            with_json_new_to_old_df.at[idx, 'current_bids_filename'] = with_json_new_to_old_df.at[
                                                                           idx, 'current_bids_filename'] + '.nii.gz'
            with_json_new_to_old_df.at[idx, 'revised_bids_filename'] = with_json_new_to_old_df.at[
                                                                           idx, 'revised_bids_filename'] + '.nii.gz'
        else:
            with_json_new_to_old_df.at[idx, 'current_bids_filename'] = with_json_new_to_old_df.at[
                                                                           idx, 'current_bids_filename'] + '.json'
            with_json_new_to_old_df.at[idx, 'revised_bids_filename'] = with_json_new_to_old_df.at[
                                                                           idx, 'revised_bids_filename'] + '.json'

    with_json_new_to_old_df.to_csv(outdir.joinpath('old_to_new_bids_filename_mapping.csv'), quoting=csv.QUOTE_MINIMAL,
                                   index=False)

    return None


if __name__ == "__main__":
    main()
