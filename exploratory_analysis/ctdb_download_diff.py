import pandas as pd
from pathlib import Path

root = Path('/Users/arshithab/Desktop/Projects/rvol/')

# CTDB downloads at two different timepoints
BASELINE_CTDB = Path(
    '/Users/arshithab/Desktop/Projects/rvol/release_2/phenotype/data/ctdb_downloads/CTDB-data-download-20211202-modified.xlsx')
FOLLOW_UP_CTDB = Path(
    '/Users/arshithab/Desktop/Projects/rvol/release_2/phenotype/data/ctdb_downloads/CTDBDataDownload_20240401.xlsx')

OUTPUT_DIR = Path('/Users/arshithab/Desktop/Projects/rvol/release_2/phenotype/lists/')


# Function borrowed from Eric Earl's listdiff utils
def diff_files(baseline, follow_up):
    with open(baseline, 'r') as list1:
        list1contents = [line.rstrip('\n') for line in list1.readlines()]

    with open(follow_up, 'r') as list2:
        list2contents = [line.rstrip('\n') for line in list2.readlines()]

    set_baseline = set(list1contents)
    set_follow_up = set(list2contents)

    set_baseline_to_2_diff = set_baseline - set_follow_up
    set_follow_up_to_1_diff = set_follow_up - set_baseline

    intersection = set_baseline & set_follow_up

    return set_baseline_to_2_diff, set_follow_up_to_1_diff


if __name__ == "__main__":

    # read in CTDB excel workbooks from two different timepoints
    baseline_dict_of_dfs = pd.read_excel(BASELINE_CTDB, skiprows=[0], sheet_name=None)
    follow_up_dict_of_dfs = pd.read_excel(FOLLOW_UP_CTDB, skiprows=[0], sheet_name=None)

    # form wise sort and parse required fields for later comparison
    for key in baseline_dict_of_dfs:
        baseline_df = baseline_dict_of_dfs[key]
        follow_up_df = follow_up_dict_of_dfs[key]

        baseline_df.sort_values(by=['SUBJECT_NUMBER', 'VISIT_DATE'], inplace=True, ignore_index=True)
        follow_up_df.sort_values(by=['SUBJECT_NUMBER', 'VISIT_DATE'], inplace=True, ignore_index=True)

        baseline_df[['SUBJECT_NUMBER', 'VISIT_DATE']].to_csv(
            root.joinpath(OUTPUT_DIR / 'baseline' / f'baseline_{key}.tsv'),
            sep='\t', index=False)
        follow_up_df[['SUBJECT_NUMBER', 'VISIT_DATE']].to_csv(
            root.joinpath(OUTPUT_DIR / 'follow_up' / f'follow_up_{key}.tsv'),
            sep='\t', index=False)

    baseline_files = OUTPUT_DIR.joinpath('baseline').glob('*.tsv')

    for baseline_file in baseline_files:
        form_name = baseline_file.name.split('baseline_')[1]
        follow_up_file = OUTPUT_DIR.joinpath(f"follow_up/follow_up_{form_name}")

        baseline_diff_follow_up, follow_up_diff_baseline = diff_files(baseline_file, follow_up_file)

        # write baseline - follow_up to file
        if len(baseline_diff_follow_up) > 0:
            with open(OUTPUT_DIR / 'baseline_diff_follow_up' / f'b_diff_f_{form_name}', 'w') as f:
                f.write(f"SUBJECT_NUMBER,VISIT_DATE\n")
                for line in baseline_diff_follow_up:
                    f.write(f"{line}\n")

        # write follow_up - baseline to file
        if len(follow_up_diff_baseline) > 0:
            with open(OUTPUT_DIR / 'follow_up_diff_baseline' / f'b_diff_f_{form_name}', 'w') as f:
                f.write(f"SUBJECT_NUMBER,VISIT_DATE\n")
                for line in follow_up_diff_baseline:
                    f.write(f"{line}\n")
