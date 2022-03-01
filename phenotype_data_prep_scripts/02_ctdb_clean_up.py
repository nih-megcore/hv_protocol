import json
from collections import defaultdict
from os import fspath
from pathlib import Path

import numpy as np
import pandas as pd

import project_filepaths as filepaths
import rvoldefinitions as rvdef


# helper functions
def compile_excluded_fields(free_text_file):
    f = open(free_text_file, 'r')
    excluded_fields = defaultdict(list)
    for line in f.readlines():
        tsvname = line.split(';')[0].strip('\'').split('.')[0]
        field = line.split(';')[1].strip('\n')
        excluded_fields[tsvname].append(field)
    return excluded_fields


def find_unnamed_cols(dict_of_dfs):
    forms_with_unnamed_cols = defaultdict(list)
    for form in dict_of_dfs.keys():
        for col in dict_of_dfs[form].columns.tolist():
            if col.startswith('Unnamed'):
                forms_with_unnamed_cols[form].append(col)
    # write to json file
    with open(Path(filepaths.curr_outputs_dir, 'forms_with_unnamed_cols.json'), 'w') as f:
        json.dump(forms_with_unnamed_cols, f, indent=4)
    return None


def get_laterality_quotient(df, version):
    """returns row index and lq value"""
    if version == 'orig':
        # print(df.columns)
        for row in range(df.shape[0]):
            rh = df[df.columns.values[[2, 4, 5, 7, 9, 12, 14, 16, 17, 19]]].values[row]
            lh = df[df.columns.values[[1, 3, 6, 8, 10, 11, 13, 15, 18, 20]]].values[row]
            rh = np.asarray([e for e in rh if e != -999], dtype=int)
            lh = np.asarray([e for e in lh if e != -999], dtype=int)
            lq = int(round(100.0 * (rh.sum() - lh.sum()) / (rh.sum() + lh.sum())))
            df.at[row, 'laterality_quotient'] = lq
        return df
    elif version == 'rev':
        # 		print(df.columns)
        for row in range(df.shape[0]):
            responses = df[df.columns.values[1:11]].values[row]
            responses = np.asarray([e for e in responses if e != -999], dtype=int)
            lq = int(round(100.0 * (responses.sum().astype(float) / np.absolute(responses).sum().astype(float))))
            df.at[row, 'laterality_quotient'] = lq
        return df


def get_handedness(df_with_lq):
    """
	lq cutoffs -
	Code-value -1 --> Left-handedness = Less than -40
	Code-value  0 --> Ambidexterity = Between -40 and +40
	Code-value  2 --> Right-handedness = More than +40
	:return:
	"""
    for ind, value in df_with_lq['handedness'].items():
        lq = df_with_lq.at[ind, 'laterality_quotient']
        if lq == -777 or lq == -999:
            df_with_lq.at[ind, 'handedness'] = lq
        elif -100 <= lq < -40:
            df_with_lq.at[ind, 'handedness'] = -1
        elif -40 <= lq <= 40:
            df_with_lq.at[ind, 'handedness'] = 0
        elif 40 < lq <= 100:
            df_with_lq.at[ind, 'handedness'] = 1
        else:
            df_with_lq.at[ind, 'handedness'] = -888  # cases where lq=-999 or -777

    return df_with_lq


if __name__ == "__main__":
    cols_renaming_record = defaultdict(dict)

    # # step 1
    # # reading ctdb spreadsheets & id mapping files into pandas dataframe
    id_linking_df = pd.read_csv(filepaths.id_filepath, low_memory=False)
    ctdb_dict_of_dfs = pd.read_excel(filepaths.ctdb_data_dir, sheet_name=None)
    legends = pd.read_excel(filepaths.ctdb_legends_dir, sheet_name=None)  # dict of dfs
    form_names_mapping = json.load(
        open(fspath(filepaths.data_dir.joinpath('mappings/ctdb_formnames_mapping.json')), 'r'))
    dict_names_mapping = json.load(
        open(fspath(filepaths.data_dir.joinpath('mappings/ctdb_dictnames_mapping.json')), 'r'))

    cols_with_demo_info = {'PATIENT_RECORD_NUMBER': ' ', 'SUBJECT_NUMBER': ' .1', 'SUBJECT_EXTERNAL_ID': ' .2',
                           'SUBJECT_ROLE': ' .3', 'SUBJECT_GROUP': ' .4', 'SUBJECT_COHORT': ' .5', 'SITE_NAME': ' .6',
                           'LAST_NAME': ' .7', 'FIRST_NAME': ' .8', 'DOB': ' .9', 'RACE': ' .10', 'ETHNICITY': ' .11',
                           'SEX': ' .12', 'AGE': ' .13', 'INTERVAL_NAME': ' .14', 'VISIT_DATE': ' .15',
                           'TIME_24_HOUR': ' .16'}
    # cleaning up multiple responses in ctdb dict of dfs
    superdupes = {'ON81734', 'ON54220', 'ON84651', 'ON98098', 'ON88331', 'ON76400', 'ON08543', 'ON99754', 'ON11394',
                  'ON98642', 'ON98454', 'ON89474', 'ON74110', 'ON62623', 'ON51005', 'ON13986', 'ON95230', 'ON11411',
                  'ON07392', 'ON25939', 'ON86202', 'ON89045', 'ON95311', 'ON88753', 'ON43131', 'ON87092', 'ON22671',
                  'ON02811', 'ON42107', 'ON85305'}

    # dealing with dupes
    fduplicates_2021 = defaultdict(lambda: defaultdict(list))
    dont_care = ["Big-Five Personality Survey", "Brief Trauma Questionnaire (BQ)",
                 "Consent V2", "Email Reminder"]
    to_be_dropped = defaultdict(list)

    # renaming zeroth row empty columns
    for form, df in ctdb_dict_of_dfs.items():

        # cleaning up multiple responses in ctdb dict of dfs
        if form not in dont_care:
            df = df[[cols_with_demo_info['SUBJECT_NUMBER'], cols_with_demo_info['LAST_NAME'],
                     cols_with_demo_info['FIRST_NAME'], cols_with_demo_info['SEX'], cols_with_demo_info['AGE'],
                     cols_with_demo_info['VISIT_DATE']]]
            for idx, rvid in df[cols_with_demo_info['SUBJECT_NUMBER']].items():
                onid = rvdef.openneuro_id_lookup(rvid)
                if onid in superdupes:
                    fduplicates_2021[form][rvid].append([df.at[idx, cols_with_demo_info['AGE']],
                                                         df.at[idx, cols_with_demo_info['VISIT_DATE']],
                                                         idx])
            # print(fduplicates_2021)
            for rvid, datalist in fduplicates_2021[form].items():
                entry_count = len(fduplicates_2021[form][rvid])
                if entry_count > 1:
                    # print(form, rvid, datalist)
                    for i in range(entry_count):
                        if datalist[i][1].startswith('2021'):
                            to_be_dropped[form].append(datalist[i][-1])

    for form, idxlist in to_be_dropped.items():
        ctdb_dict_of_dfs[form] = ctdb_dict_of_dfs[form].drop(index=idxlist)

    # step 2
    # renaming survey legends to standard names for readability
    for stdname, value in dict_names_mapping.items():
        if type(value) == dict and value['ctdb'] in legends.keys():
            legends[value['openneuro']] = legends[value['ctdb']]
            del legends[value['ctdb']]
        else:
            legends[value] = legends[stdname]
            del legends[stdname]

    # renaming surveys with industry standard names for readability
    forms_to_be_discarded = list(ctdb_dict_of_dfs.keys())
    for stdname, value in form_names_mapping.items():
        if type(value) == dict and value['ctdb'] in ctdb_dict_of_dfs.keys():
            ctdb_dict_of_dfs[value['openneuro']] = ctdb_dict_of_dfs[value['ctdb']]
            del ctdb_dict_of_dfs[value['ctdb']]
            forms_to_be_discarded.remove(value['ctdb'])
        else:
            ctdb_dict_of_dfs[value] = ctdb_dict_of_dfs[stdname]
            del ctdb_dict_of_dfs[stdname]
            forms_to_be_discarded.remove(stdname)

    for f in forms_to_be_discarded:
        ctdb_dict_of_dfs.pop(f, None)

    # step 3
    # compile and remove fields with free text containing any PII
    # also remove cols with demographic info
    fields_to_be_dropped = compile_excluded_fields(filepaths.free_text_list)
    for form_name, df in ctdb_dict_of_dfs.items():
        to_be_dropped = [col for col in ctdb_dict_of_dfs[form_name].columns
                         if col != ' .1' and col.startswith((' ', ' .'))]  # fields with demo info
        if form_name in fields_to_be_dropped.keys():
            to_be_dropped.extend(fields_to_be_dropped[form_name])
        ctdb_dict_of_dfs[form_name] = rvdef.remove_freetext_fields(ctdb_dict_of_dfs[form_name], set(to_be_dropped))
        ctdb_dict_of_dfs[form_name] = ctdb_dict_of_dfs[form_name].rename(columns={' .1': ' '})
        ctdb_dict_of_dfs[form_name]['participant_id'] = ctdb_dict_of_dfs[form_name].loc[1:, ' ']
        del ctdb_dict_of_dfs[form_name][' ']
        ctdb_dict_of_dfs[form_name].drop([0], inplace=True)  # drop row with questions

# step 4
# tranform spreadsheet with ctdb legends to bids format data dictionaries
rvdef.transform_ctdb_legends(legends, dict_names_mapping)

# step 5
# data cleaning steps common to both cris and ctdb data
clean_ctdb_df = rvdef.data_clean_up(ctdb_dict_of_dfs, filepaths.ctdb_out_dir)
rvdef.create_tsvs('ctdb', clean_ctdb_df, filepaths.ctdb_out_dir)
# print(clean_ctdb_df.keys())
# adding a new empty column
ehi_forms = ['ehi', 'ehi_r']
for form_name in ehi_forms:
    clean_ctdb_df[form_name]['laterality_quotient'] = -999
    if form_name == 'ehi':
        clean_ctdb_df[form_name] = get_laterality_quotient(clean_ctdb_df[form_name], 'orig')
    elif form_name == 'ehi_r':
        clean_ctdb_df[form_name] = get_laterality_quotient(clean_ctdb_df[form_name], 'rev')
    curr_order = clean_ctdb_df[form_name].columns.tolist()
    req_order = [curr_order[0]] + [curr_order[-1]] + curr_order[1:-1]
    clean_ctdb_df[form_name] = clean_ctdb_df[form_name].loc[:, req_order]
    clean_ctdb_df[form_name]['handedness'] = -999  # new handedness column initialized with -999s
    curr_order = clean_ctdb_df[form_name].columns.tolist()
    req_order = [curr_order[0]] + [curr_order[-1]] + curr_order[1:-1]
    clean_ctdb_df[form_name] = get_handedness(clean_ctdb_df[form_name]).loc[:, req_order]

rvdef.create_tsvs('ctdb', clean_ctdb_df, filepaths.ctdb_out_dir)

# combine survey with orig and revised versio
rvdef.combine_demographics()
rvdef.combine_whodas()
rvdef.combine_ehi()

# finding unnamed columns across ctdb data and writing it to a json file
find_unnamed_cols(clean_ctdb_df)
