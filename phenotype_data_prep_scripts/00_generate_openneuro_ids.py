import csv
import hashlib
import time
from itertools import permutations
from os import fspath

import numpy as np
import pandas as pd

import rvoldefinitions as rvdef

pd.set_option('display.max_columns', None)


# helper functions
def isduplicate(inp):
    """Checks for duplicates for an input list"""
    dups = set([e for e in inp if inp.count(e) > 1])
    return list(dups)


def generate_onid(onidlist, rvid):
    """Checks for duplicates for an input list"""
    hashcode = int(hashlib.sha256(rvid.encode('utf-8')).hexdigest(), 16) % 100000
    perms = set([''.join(c) for c in permutations(str(hashcode))])
    perms = sorted([int(p) for p in perms], reverse=True)
    ctr = 0
    onid = f'ON{perms[ctr]:05d}'
    # check for any potential duplicates
    while onid in onidlist:
        ctr += 1
        onid = f'ON{perms[ctr]:05d}'
    return onid


if __name__ == "__main__":
    id_linking_df = rvdef.id_mapping

    # reading in CTDB data as a dictionary of dataframes. Each dataframe contains responses to questionnaires.
    # 'SUBJECT_NUMBER' field contains the RVIDs of the participants. 
    ctdb_all_df = pd.read_excel(rvdef.filepaths.ctdb_data_dir, skiprows=[1], sheet_name=None)
    onid_mapping = {}
    unique_rvids_in_data = set()  # set of unique RVol IDs

    # crawl through all ctdb forms to find list of unique RVIDs
    for form, df in ctdb_all_df.items():
        df['participant_id'] = df[' ']
        del df[' ']
        for ind, snum in df['participant_id'].items():
            unique_rvids_in_data.add(snum)

    print(f'No. of unique subjects across CTDB questionnaires is {len(unique_rvids_in_data)}')
    unique_rvids_in_id_file = id_linking_df['SUBJECT_NUMBER']
    existing_onids = id_linking_df['open_neuro_id'].tolist()

    # gives a list of rvids in ctdb data NOT present in id_linking_file
    no_onids_subjs = np.setdiff1d(list(unique_rvids_in_data), unique_rvids_in_id_file).tolist()

    # verifies if there are any duplicate openneuro_ids in the current id_linking_file
    dupes = isduplicate(existing_onids)
    if dupes:
        print(dupes)
        print(f'ALERT! There are duplicates in your id_linking_file. Inspect {id_file} for these IDs {dups} \
        and find a resolution before proceeding')
    else:
        for ind, rvid in unique_rvids_in_id_file.items():
            onid_mapping[rvid] = id_linking_df.at[ind, 'open_neuro_id']

        if no_onids_subjs:
            for rvid in no_onids_subjs:
                onid = generate_onid(existing_onids, rvid)
                existing_onids.append(onid)
                onid_mapping[rvid] = onid

    # writing to a csv file
    timestr = time.strftime('%Y%m%d_%H%M%S')
    with open(fspath(rvdef.filepaths.data_dir.joinpath('id_files', 'id_linking_file_' + timestr + '.csv')), 'w',
              newline='') as csvfile:
        header = ['SUBJECT_NUMBER', 'open_neuro_id']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for key, value in onid_mapping.items():
            writer.writerow({'SUBJECT_NUMBER': key, 'open_neuro_id': value})
