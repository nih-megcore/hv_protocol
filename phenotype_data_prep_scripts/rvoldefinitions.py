import csv
import json
from collections import defaultdict
from os import fspath
from pathlib import Path

import pandas as pd

import project_filepaths as filepaths

# reading id_linking_file as a data frame
id_mapping = pd.read_csv(filepaths.id_filepath, low_memory=False)
rvs_to_be_shared = id_mapping['SUBJECT_NUMBER'].tolist()

# participants to be excluded from CTDB and CRIS data
combined_forms = ['ehi.tsv', 'ehi_r.tsv', 'whodas.tsv', 'whodas_r.tsv', 'demographics.tsv', 'demographics_r.tsv']


# definitions used for data cleaning
def openneuro_id_lookup(rvid):
    """given a rvid return the corresponding openneuro id"""
    onid = id_mapping.loc[id_mapping['SUBJECT_NUMBER'] == rvid, 'openneuro_id'].values[0]
    return onid


def rvid_lookup(onid):
    """given an openneuro_id return the corresponding rvid"""
    rvid = id_mapping.loc[id_mapping['openneuro_id'] == onid, 'SUBJECT_NUMBER'].values[0]
    return rvid


def duplicate_onids():
    # TODO: load openneuroids from id linking file and verify that there are no duplicates
    # returns either an empty list or non empty list with rvids that have the same
    # openneuro id
    # this function will be called after a new id linking file has been created
    # and before regenerating tsvs
    return None


def duplicate_rvids():
    # TODO: load rvid from id linking file and verify that there are no duplicates
    return None


def new_subjs_check():
    # TODO: find a list of all subjects in the new downloads
    # TODO: compare it with subjects available in participants.tsv
    # TODO: if any new subjects, then create a new id linking file with the new subjects
    return None


def remove_nans(dict_of_dfs):
    """replaces NaNs from a dictionary of dataframes"""
    for key, df in dict_of_dfs.items():
        dict_of_dfs[key] = dict_of_dfs[key].fillna(-999)
    return dict_of_dfs


def reorder_cols(df):
    """places the `participant_id` column as the first column"""
    # print(df.columns)
    req_order = [df.columns.tolist()[-1]] + df.columns.tolist()[:-1]
    # print(req_order)
    df = df.loc[:, req_order]
    df = df.sort_values(by=['participant_id'], ignore_index=True)
    return df


def remove_blank_rows(df):
    """remove participants that have no data available aka blank rows"""
    clean_df = df.filter(df.columns[1:], axis=1).dropna(how='all', axis=0)
    idx_to_keep = clean_df.index
    clean_df = df.filter(idx_to_keep, axis=0)
    return clean_df


def multiple_subj_responses(modality):
    if modality == 'cris':
        tsvs = list(filepaths.cris_out_dir.glob('*.tsv'))
    elif modality == 'ctdb':
        tsvs = list(filepaths.ctdb_out_dir.glob('*.tsv'))

    d = defaultdict(list)
    for tsv in tsvs:
        df = pd.read_csv(fspath(tsv), sep='\t')
        duplicate_ind = []
        for ind, val in df.duplicated(subset=['participant_id']).items():
            if val: duplicate_ind.append(ind)
        dupes = list(df.loc[df.duplicated(subset=['participant_id']), 'participant_id'])
        if dupes:
            if tsv.name not in combined_forms:
                for onid in dupes:
                    rvid = rvid_lookup(onid.split('-')[1])
                    d[tsv.name].append(f'{onid}: {rvid}')
    with open(filepaths.curr_outputs_dir.joinpath(modality + '_multiple_responses_found.json'), 'w') as f:
        json.dump(d, f, indent=4)


def create_cris_data_dict(df, filename, outdir):
    """create a json data dictionary for a given cris dataframe"""
    json_dict = {}
    for key in df.keys():
        if key != 'participant_id':
            json_dict[key] = {'Units': key.split()[-1]}
        else:
            json_dict[key] = {'Description': 'OpenNeuro ID of the subject.'}
    with open(outdir.joinpath(filename + '.json'), "w") as f:
        json.dump(json_dict, f, indent=4)


def transform_ctdb_legends(dict_of_legends, dict_names_mapping):
    columns = []
    for form_name, legend in dict_of_legends.items():
        df = dict_of_legends[form_name]  # same as `legend`
        columns += list(df.columns)

    header = list(set(columns))
    for form_name, legend in dict_of_legends.items():
        unused_ctdb_legends = {}
        for stdname, values in dict_names_mapping.items():
            if form_name == values['openneuro']:
                print(form_name)

                df = dict_of_legends[form_name]
                df.drop(df.shape[0] - 1)
                out_filename = Path(filepaths.ctdb_out_dir, form_name + '.json')
                qid_uniq = df['QUESTIONID'].unique()  # compile unique qids for the survey
                qids = qid_uniq[qid_uniq != ' '].astype('int')

                d = {}
                d['participant_id'] = {'Description': 'OpenNeuro ID of the subject.'}
                current = ''
                for i, row in df.iterrows():
                    # detecting if on first line of data dictionary/legend
                    if current == '':
                        # start
                        qid = str(int(row['QUESTIONID']))
                        current = qid
                        if pd.isna(row['QUESTION_ALIAS']):
                            ShortName = row['QUESTION_NAME']
                        else:
                            ShortName = row['QUESTION_ALIAS']
                        LongName = row['QUESTION_NAME'] + ' (question ID ' + qid + ')'
                        Description = row['QUESTION_TEXT']
                        Levels = None

                    elif not pd.isna(row['QUESTION_TEXT']):
                        # write
                        d[ShortName] = {}
                        d[ShortName]['LongName'] = LongName
                        d[ShortName]['Description'] = Description
                        if Levels:
                            d[ShortName]['Levels'] = Levels
                        # reset
                        qid = str(int(row['QUESTIONID']))
                        if pd.isna(row['QUESTION_ALIAS']):
                            ShortName = row['QUESTION_NAME']
                        else:
                            ShortName = row['QUESTION_ALIAS']
                        LongName = row['QUESTION_NAME'] + ' (question ID ' + qid + ')'
                        Description = row['QUESTION_TEXT']
                        # DataType = row[10]
                        # Range = row[12]
                        Levels = None

                    if not Levels:
                        if not pd.isna(row['CODEVALUE']):
                            if type(row['DISPLAY']) == float:
                                if pd.isna(row['DISPLAY']):
                                    Levels = {str(int(row['CODEVALUE'])): 'N/A'}
                                else:
                                    Levels = {str(int(row['CODEVALUE'])): str(int(row['DISPLAY']))}
                            else:
                                Levels = {str(int(row['CODEVALUE'])): str(row['DISPLAY'])}
                    else:
                        if not pd.isna(row['CODEVALUE']):
                            if type(row['DISPLAY']) == float:
                                if pd.isna(row['DISPLAY']):
                                    Levels[str(int(row['CODEVALUE']))] = 'N/A'
                                else:
                                    Levels[str(int(row['CODEVALUE']))] = str(int(row['DISPLAY']))
                            else:
                                Levels[str(int(row['CODEVALUE']))] = str(row['DISPLAY'])
                    # detecting if on last line of data dictionary/legend
                    if i == df.shape[0] - 1:
                        # write
                        d[ShortName] = {}
                        d[ShortName]['LongName'] = LongName
                        d[ShortName]['Description'] = Description
                        if Levels:
                            d[ShortName]['Levels'] = Levels
                        with open(fspath(out_filename), 'w') as f:
                            json.dump(d, f, indent=4)
        else:
            unused_ctdb_legends[form_name] = form_name.replace(' ', '_') + '.json'
            with open(fspath(filepaths.curr_outputs_dir.joinpath('unused_ctdb_surveys.json')), 'w') as f:
                f.write(json.dumps(unused_ctdb_legends, indent=4))


def remove_freetext_fields(form_df, excl_fields):
    form_df = form_df.drop(columns=excl_fields, axis=1)
    return form_df


def data_clean_up(dict_of_dfs, outdir):
    """
    - reorder columns so that `participant_id` col comes before all other cols
    - replace NaNs with '-999'
    - replace RV subject ids with openneuro ids
    - remove blank lines
    """
    # rvs_to_be_shared = id_mapping['SUBJECT_NUMBER'].tolist()
    for key, df in dict_of_dfs.items():
        for ind, subjnum in df['participant_id'].items():
            if subjnum in rvs_to_be_shared:
                onid = openneuro_id_lookup(subjnum)
                if onid:
                    dict_of_dfs[key].at[ind, 'participant_id'] = '-'.join(['sub', onid])
            else:
                dict_of_dfs[key] = dict_of_dfs[key].drop(index=ind, axis=0)
        dict_of_dfs[key] = reorder_cols(dict_of_dfs[key])
        dict_of_dfs[key] = remove_blank_rows(dict_of_dfs[key])
    dict_of_dfs = remove_nans(dict_of_dfs)
    return dict_of_dfs


def create_tsvs(modality, dict_of_dfs, outdir):
    """create a tsv file for each dataframe in the dictionary"""
    if modality == 'ctdb':
        # multiple_subj_responses(modality)
        for form_name, df in dict_of_dfs.items():
            df.to_csv(outdir.joinpath(form_name + '.tsv'), sep='\t', quoting=csv.QUOTE_MINIMAL, index=False)

    elif modality == 'cris':
        # multiple_subj_responses(modality)
        for labtest, df in dict_of_dfs.items():
            create_cris_data_dict(dict_of_dfs[labtest], labtest, outdir)
            df.to_csv(fspath(outdir.joinpath(labtest + '.tsv')), sep='\t', quoting=csv.QUOTE_MINIMAL, index=False)


def drop_overlap_subj(revd_df, intersections_file):
    # int_file = Path(filepaths.data_dir, 'overlapping_subjects.txt')
    subjlist = pd.read_csv(fspath(intersections_file), sep=' ', header=None)[0].values.tolist()
    for ind, subj in revd_df['participant_id'].items():
        if subj in subjlist:
            revd_df = revd_df.drop(ind, axis=0)
    return revd_df


def combine_whodas():
    orig_tsv = filepaths.ctdb_out_dir.joinpath('whodas.tsv')
    orig_dict = json.load(open(fspath(filepaths.ctdb_out_dir.joinpath('whodas.json')), 'r'))
    revd_tsv = filepaths.ctdb_out_dir.joinpath('whodas_r.tsv')
    revd_dict = json.load(open(fspath(filepaths.ctdb_out_dir.joinpath('whodas_r.json')), 'r'))

    fields_mapping = {}
    for key, subj in orig_dict.items():
        if key != 'participant_id':
            fields_mapping[subj['LongName'].split()[0]] = key

    # modify revd json dictionary
    old_keys = list(revd_dict.keys())
    for key in old_keys:
        if key != 'participant_id':
            revd_dict[fields_mapping[key]] = revd_dict[key]
            del revd_dict[key]

    # write to json file
    with open(fspath(filepaths.ctdb_out_dir.joinpath('whodas_combined.json')), 'w') as f:
        json.dump(revd_dict, f, indent=4)

    # combine tsvs
    revd_df = pd.read_csv(revd_tsv, sep='\t')
    orig_df = pd.read_csv(orig_tsv, sep='\t')
    old_cols = revd_df.columns
    new_cols = ['participant_id']
    for col in old_cols[1:]:
        new_cols.append(fields_mapping[col])
    revd_df.columns = new_cols

    # drop rows with overlapping subjects
    revd_df = drop_overlap_subj(revd_df,
                                filepaths.data_dir.joinpath('survey_combinations_data/whodas_overlapping_subjs.txt'))
    combined_df = pd.concat([orig_df, revd_df], ignore_index=True)
    combined_df = combined_df.sort_values(by=['participant_id'], ignore_index=True)
    combined_df.to_csv(fspath(filepaths.ctdb_out_dir.joinpath('whodas_combined.tsv')), sep='\t',
                       quoting=csv.QUOTE_MINIMAL, index=False, mode='w')


def combine_demographics():
    orig_df = pd.read_csv(filepaths.ctdb_out_dir.joinpath('demographics.tsv'), sep='\t')
    revd_df = pd.read_csv(filepaths.ctdb_out_dir.joinpath('demographics_r.tsv'), sep='\t')
    # print(revd_df.columns)
    with open(filepaths.data_dir.joinpath('mappings', 'demographics_mappings.json'), 'r') as f:
        mapping = json.load(f)

    orig_df.rename(columns=mapping, inplace=True)
    # print(orig_df.columns)
    orig_df['SETTING'] = orig_df['SETTING'].mask(orig_df['SETTING'] == -999, other=orig_df['Unnamed: 32'])
    del orig_df['Unnamed: 32']
    # print(orig_df)
    revd_df = drop_overlap_subj(revd_df,
                                filepaths.data_dir.joinpath('survey_combinations_data/demo_overlapping_subjs.txt'))

    combined_df = orig_df.append(revd_df, sort=False, ignore_index=True)
    combined_df.fillna(-777, inplace=True)

    for column in ['CURRENT_GENDER_2', 'LGBT_IDENTITY_2', 'RACE_1_2', 'RACE_1_3', 'RACE_1_4',
                   'REFERRAL_TYPE_SECONDARY_4']:
        combined_df[column] = combined_df[column].mask(combined_df[column] == -777, other=-999)
        combined_df[column] = combined_df[column].astype(int)
    combined_df = combined_df.sort_values(by=['participant_id'], ignore_index=True)
    combined_df.to_csv(fspath(filepaths.ctdb_out_dir.joinpath('demographics_combined.tsv')), sep='\t',
                       quoting=csv.QUOTE_MINIMAL, index=False)


def combine_ehi():
    orig_df = pd.read_csv(filepaths.ctdb_out_dir.joinpath('ehi.tsv'), sep='\t')
    revd_df = pd.read_csv(filepaths.ctdb_out_dir.joinpath('ehi_r.tsv'), sep='\t')

    revd_df = drop_overlap_subj(revd_df,
                                filepaths.data_dir.joinpath('survey_combinations_data/ehi_overlapping_subjs.txt'))
    combined_df = pd.concat([orig_df, revd_df], ignore_index=True).fillna(-777)
    for col in combined_df.columns.tolist()[1:]:
        combined_df[col] = combined_df[col].astype(int)
    new_combined_header = \
        pd.read_csv(filepaths.data_dir.joinpath('survey_combinations_data/ehi_columns_order.csv'), header=None)[
            0].values.tolist()
    combined_df.columns = new_combined_header
    combined_df = combined_df.sort_values(by=['participant_id'], ignore_index=True)
    combined_df.to_csv(fspath(filepaths.ctdb_out_dir.joinpath('ehi_combined.tsv')), sep='\t', quoting=csv.QUOTE_MINIMAL,
                       index=False)
