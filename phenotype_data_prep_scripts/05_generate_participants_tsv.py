import csv
import os
import re
import time
from collections import defaultdict

import pandas as pd

import project_filepaths as filepaths

phenotype_tsvs = list(filepaths.work_dir.joinpath('bids_phenotype/phenotype/').glob('*.tsv'))
imaging_subjs_onids = pd.read_csv(filepaths.data_dir.joinpath('id_files/mri_155_toshare.csv'))['openneuro_id'].tolist()
meg_subjs_onids = pd.read_csv(filepaths.data_dir.joinpath('id_files/meg_67_toshare.csv'))['openneuro_id'].tolist()

# compile unique subject IDs from all of the tsvs
phenotype_unique_onids = defaultdict(set)
for p in phenotype_tsvs:
    df = pd.read_csv(os.fspath(p), sep='\t')
    for i, onid in df['participant_id'].items():
        if p.name == 'eligibility.tsv':
            if df.at[i, 'eligibility'] == 1:
                phenotype_unique_onids[p.name].add(onid.strip())  # including only eligible subjects
        else:
            phenotype_unique_onids[p.name].add(onid.strip())

# creating a participant counts summary for surveys, labtests, imaging and meg
counts = defaultdict(int)
timestr = time.strftime('%Y%m%d')
counts['MRI'] = int(len(imaging_subjs_onids))
counts['MEG'] = int(len(meg_subjs_onids))
for key, value in phenotype_unique_onids.items():
    counts[key.split('.')[0]] = int(len(phenotype_unique_onids[key]))

counts_df = pd.DataFrame(counts.values(), index=counts.keys(), columns=['participant_cts']).sort_values(
    by=['participant_cts'])
counts_df.to_csv(filepaths.curr_outputs_dir.joinpath('subjects_counts_' + timestr + '.csv'), quoting=csv.QUOTE_ALL)
# participants_df initialization and assignment
full_participants_list = set()
for onid in imaging_subjs_onids:
    full_participants_list.add(onid)  # adding imaging subjects to participants list

for onid in meg_subjs_onids:
    full_participants_list.add(onid)  # adding meg subjects to participants list

for key, value in phenotype_unique_onids.items():
    for onid in value:
        full_participants_list.add(onid)

# writing all participants to file
all_pids_filepath = filepaths.data_dir.joinpath('id_files', 'all_participants_onids.txt')
with open(os.fspath(all_pids_filepath), 'w') as f:
    for pid in full_participants_list: f.write(f'{pid}\n')

# extending columns of participants_df
participant_tsv_cols = ['participant_id', 'age', 'sex', 'handedness', 'eligibility', 'MRI', 'MEG']
participant_tsv_cols.extend([k.split('.')[0] for k in sorted(phenotype_unique_onids.keys()) if k != 'eligibility.tsv'])
participants_df = pd.DataFrame(columns=participant_tsv_cols)

# initializing empty rows by filling in partcipants_id column
all_pids_df = pd.read_csv(all_pids_filepath, sep=' ', header=None)
all_pids_df.sort_values(by=[0], ignore_index=True)
# print(len(all_pids_df))
participants_df['participant_id'] = all_pids_df.loc[:, 0]

# filling in cells of the participants_df
for test, onid_set in phenotype_unique_onids.items():
    test = test.split('.')[0]
    for each in onid_set:
        rowind = participants_df[participants_df['participant_id'] == each].index[0]
        participants_df.at[rowind, test] = 1
    participants_df[test] = participants_df[test].fillna(0)

for each in imaging_subjs_onids:
    rowind = participants_df[participants_df['participant_id'] == each].index[0]
    participants_df.at[rowind, "MRI"] = 1
    participants_df["MRI"] = participants_df["MRI"].fillna(0)

for each in meg_subjs_onids:
    rowind = participants_df[participants_df['participant_id'] == each].index[0]
    participants_df.at[rowind, "MEG"] = 1
    participants_df["MEG"] = participants_df["MEG"].fillna(0)

# check for rows that sum up to zero or, in other words, are empty
for ind in participants_df.index:
    row_sum = participants_df.loc[ind, participants_df.columns.tolist()[4:]].sum()
    if row_sum == 0:
        print(f"{participants_df.at[ind, 'participant_id']} sums up to {row_sum} and needs to be dropped")
        participants_df = participants_df.drop([ind], axis=0)

interested_cols = ['AGE', 'GENDER']
demo_df = pd.read_csv(filepaths.work_dir.joinpath('bids_phenotype/phenotype/demographics.tsv'), sep='\t')
ehi_df = pd.read_csv(filepaths.work_dir.joinpath('bids_phenotype/phenotype/ehi.tsv'), sep='\t')
all_pids = all_pids_df[0].values.tolist()

for ind, pid in demo_df['participant_id'].items():
    if pid in all_pids:
        for col in interested_cols:
            if col == 'GENDER':
                if demo_df.at[ind, col] == 1:
                    sex = 'male'
                elif demo_df.at[ind, col] == 2:
                    sex = 'female'
                else:
                    sex = 'n/a'
                participants_df.loc[participants_df['participant_id'] == pid, 'sex'] = sex
            else:
                if demo_df.at[ind, col] == '-999':
                    age = 'n/a'
                else:
                    age = demo_df.at[ind, col]
                participants_df.loc[participants_df['participant_id'] == pid, col.lower()] = re.sub(',', '', age)

for ind, pid in ehi_df['participant_id'].items():
    if pid in all_pids:
        if ehi_df.at[ind, 'handedness'] == 1:
            handedness = 'right'
        elif ehi_df.at[ind, 'handedness'] == 0:
            handedness = 'ambidextrous'
        elif ehi_df.at[ind, 'handedness'] == -1:
            handedness = 'left'
        else:
            handedness = 'n/a'
        participants_df.loc[participants_df['participant_id'] == pid, 'handedness'] = handedness

# sorting by participant_ids and filling residual NaNs with appropriate codes
participants_df.sort_values(by=['participant_id'], ignore_index=True, inplace=True)
participants_df.age = participants_df.age.fillna('n/a')
participants_df.sex = participants_df.sex.fillna('n/a')
participants_df.handedness = participants_df.handedness.fillna('n/a')

# writing to file
participants_df.to_csv(filepaths.work_dir.joinpath('bids_phenotype/participants.tsv'), sep='\t',
                       quoting=csv.QUOTE_MINIMAL, index=False)

# generate basic stats from the participants tsv as verification
subject_ct = len(participants_df.participant_id.unique())
sex_value_cts = participants_df.value_counts(subset=['sex'], dropna=False)
age_value_cts = participants_df.value_counts(subset=['age'], dropna=False)
eligibility_value_cts = participants_df.value_counts(subset=['eligibility'], dropna=False)
handedness_value_cts = participants_df.value_counts(subset=['handedness'], dropna=False)
mri_value_cts = participants_df.value_counts(subset=['MRI'], dropna=False)
meg_value_cts = participants_df.value_counts(subset=['MEG'], dropna=False)
summary_participants_tsv = [sex_value_cts, age_value_cts, eligibility_value_cts, handedness_value_cts,
                            mri_value_cts, meg_value_cts]

for i in range(len(summary_participants_tsv)):
    field_name = summary_participants_tsv[i].keys().names[0]
    print(f"{field_name}")
    for idx, value in summary_participants_tsv[i].items():
        print(idx[0], value)
    print()
