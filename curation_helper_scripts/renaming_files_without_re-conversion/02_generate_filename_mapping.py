import argparse
import csv
import re
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description="Does something worth doing.")

    parser.add_argument("--input_dir", type=Path, action='store', dest='inputdir', help="Path to input directory.")
    parser.add_argument("--output_dir", type=Path, action='store', dest='outdir', help="Path to output directory.")

    args = parser.parse_args()
    return args.inputdir, args.outdir


def run_shell_cmd(cmdstr):
    pipe = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, encoding='utf8', shell=True)
    return pipe.stdout


def main():
    inputdir, outdir = parse_arguments()
    json_data = inputdir.joinpath('data/17M081_jsons')

    series_descriptions = inputdir.joinpath('data/all_series_descriptions.txt')
    series_filenames = list(json_data.joinpath('series_to_filenames').glob('*.txt'))

    df_columns = ['original_series_description', 'modified_series_description', 'current_bids_filename',
                  'revised_common_identifiers', 'revised_bids_filename']
    df = pd.DataFrame(columns=df_columns)
    idx = 0
    for series_filename in series_filenames:
        desc = series_filename.name.split('.')[0]
        f = open(series_filename, 'r')
        for line in f.readlines():
            df.at[idx, 'current_bids_filename'] = line.strip().split('./')[1]
            df.at[idx, 'modified_series_description'] = desc
            idx += 1

    series_to_identifier_df = pd.read_csv(inputdir.joinpath('data/series_descriptions_to_new_common_identifiers.csv'))
    series_to_identifier_df.to_csv(outdir.joinpath('series_descriptions_to_revised_identifiers.csv'),
                                   quoting=csv.QUOTE_MINIMAL, index=False)

    grouped_df = df.groupby(by=['modified_series_description'])
    unique_series_desc = grouped_df.groups.keys()
    for series_desc in unique_series_desc:
        for idx in grouped_df.groups[series_desc]:
            curr_filename = df.at[idx, 'current_bids_filename']
            prefix = '_'.join(curr_filename.split('_')[:2])
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

    with_json_new_to_old_df.to_csv('scripts_output/old_to_new_bids_filename_mapping.csv', quoting=csv.QUOTE_MINIMAL,
                                   index=False)

    return None


if __name__ == "__main__":
    main()
