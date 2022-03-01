import pandas as pd
import rvoldefinitions as rvdef
import project_filepaths as filepaths
from collections import defaultdict
import json
import re
from os import fspath


# helper functions
def format_cris_data(dict_of_dfs):
    # removing trailing spaces from fieldnames
    for form_name, df in dict_of_dfs.items():
        # find "< " and replace with "<"
        p = re.compile(r'<\s')
        df = df.replace(to_replace=p, value='<', regex=True)
        for field in df.columns.tolist():
            if field != 'participant_id':
                df[field] = df[field].str.upper()
        dict_of_dfs[form_name] = df
    return dict_of_dfs


if __name__ == "__main__":

    # reading necessary files into pandas dataframe
    id_linking_df = pd.read_csv(filepaths.id_filepath, low_memory=False)
    cris_df = pd.read_excel(filepaths.cris_data_dir, header=None)
    cris_mapping_path = filepaths.data_dir.joinpath('mappings/cris_formnames_mapping.json')
    cris_formnames_mapping = json.load(open(fspath(cris_mapping_path)))

    # pulling out lab test names' column indices
    ind_testnames = defaultdict(list)
    for i, v in enumerate(cris_df.iloc[0, 6:]):
        ind_testnames[v].append(i)

    # renaming cris forms to standard names
    orig_filenames = list(ind_testnames.keys())
    for stdname in cris_formnames_mapping.keys():
        for testname in orig_filenames:
            if testname == cris_formnames_mapping[stdname]['cris']:
                ind_testnames[cris_formnames_mapping[stdname]['openneuro']] = ind_testnames[testname]
                del ind_testnames[testname]

    # creating a dictionary of dataframes for each lab test from a single spreadsheet
    cris_dfs_dict = defaultdict(lambda: pd.DataFrame())
    for form_name, idx in ind_testnames.items():
        idx = [6 + int(val) for val in idx]
        header = [field.strip() for field in cris_df.iloc[1, idx]]
        cris_dfs_dict[form_name] = cris_df.iloc[3:, idx]
        cris_dfs_dict[form_name].columns = header
        cris_dfs_dict[form_name]['participant_id'] = cris_df.iloc[3:, 0]  # add participant ids to column
    # print(cris_dfs_dict)
    cris_dfs_dict = format_cris_data(cris_dfs_dict)
    
    #
    clean_cris_dfs_dict = rvdef.data_clean_up(cris_dfs_dict, filepaths.cris_out_dir)
    rvdef.create_tsvs('cris', clean_cris_dfs_dict, filepaths.cris_out_dir)