import csv
import os
import shutil

import pandas as pd

import project_filepaths as filepaths

# 1. copy ineligible.tsv and json and, the data dictionaries for combined surveys
files_to_be_copied = ['ehi_combined.json',
                      'demographics_combined.json', 'whodas_combined.json',
                      'health_history_questions.json', 'eligibility.tsv', 'eligibility.json']
for file in files_to_be_copied:
    shutil.copy2(filepaths.data_dir.joinpath('survey_combinations_data', file), filepaths.ctdb_out_dir)

# 2. delete surveys with 2 versions
files_to_be_deleted = ['whodas_r.json', 'whodas.json', 'whodas.tsv', 'whodas_r.tsv', 'ehi_r.tsv', 'ehi_r.json',
                       'ehi.json', 'ehi.tsv', 'demographics.json',
                       'demographics_r.tsv', 'demographics_r.json', 'demographics.tsv']
keywords = ('demographics', 'ehi', 'whodas')
for file in files_to_be_deleted:
    os.remove(os.fspath(filepaths.ctdb_out_dir.joinpath(file)))

# 3. rename '_combined' versions
for file in filepaths.ctdb_out_dir.iterdir():
    if file.name.startswith(keywords):
        file.rename(filepaths.ctdb_out_dir.joinpath('.'.join(file.name.split('_combined.'))))

# 4. correct the age of a participant in demographics file
correction = {'participant_id': 'sub-ON17159', 'age': 24}
demographics_df = pd.read_csv(filepaths.ctdb_out_dir.joinpath('demographics.tsv'), sep='\t')
for ind, subj in demographics_df.participant_id.items():
    if subj == correction['participant_id']:
        demographics_df.at[ind, 'AGE'] = correction['age']
demographics_df.to_csv(filepaths.ctdb_out_dir.joinpath('demographics.tsv'), sep='\t',
                       quoting=csv.QUOTE_MINIMAL, index=False)

# 5. remove unnamed columns in mental_health_questions.tsv
mental_health_df = pd.read_csv(filepaths.ctdb_out_dir.joinpath('mental_health_questions.tsv'), sep='\t').drop(
    columns=['Unnamed: 28', 'Unnamed: 30'])
mental_health_df.to_csv(filepaths.ctdb_out_dir.joinpath('mental_health_questions.tsv'), sep='\t',
                        quoting=csv.QUOTE_MINIMAL, index=False)

# remove kbit duplicate rows
kbit_duplicates = ['ON07392', 'ON22671', 'ON42107', 'ON74110', 'ON88331', 'ON98642', 'ON9975']
kbit_df = pd.read_csv(filepaths.ctdb_out_dir.joinpath('kbit2_vas.tsv'), sep='\t')
seen = set()
kbit_idx_dropped = []
for idx, pid in kbit_df['participant_id'].items():
    seen.add(pid)
    if pid.split('-')[1] in kbit_duplicates and pid not in seen:
        kbit_idx_dropped.append(pid.split('-')[1])
kbit_df.drop(kbit_idx_dropped, axis=0, inplace=True)
kbit_df.to_csv(filepaths.ctdb_out_dir.joinpath('kbit2_vas.tsv'), sep='\t',
               quoting=csv.QUOTE_MINIMAL, index=False)
