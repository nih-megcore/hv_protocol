import pandas as pd
from pathlib import Path

RELEASE_1 = Path('/Users/arshithab/Desktop/Projects/rvol/release_1/ds004215/')
ID_FILE = Path(
    '/Users/arshithab/Desktop/Projects/rvol/release_2/phenotype/data/id_files/id_linking_file_20240402_171021.csv')  # latest id_linking_file

if __name__ == "__main__":

    RELEASE_1 = Path('/Users/arshithab/Desktop/Projects/rvol/release_1/ds004215/')
    ID_FILE = Path(
        '/Users/arshithab/Desktop/Projects/rvol/release_2/phenotype/data/id_files/id_linking_file_20240402_171021.csv')  # latest id_linking_file

    id_map_df = pd.read_csv(ID_FILE)

    baseline_participants_df = pd.read_csv(RELEASE_1 / 'participants.tsv', sep='\t')
    baseline_onids = [onid.split('-')[1] for onid in baseline_participants_df.participant_id.tolist()]
    baseline_rvids = [id_map_df.loc[id_map_df['openneuro_id'] == onid, 'SUBJECT_NUMBER'].values[0] for onid in
                      baseline_onids]

    all_rvids = id_map_df.SUBJECT_NUMBER.tolist()

    follow_up_rvids = set(all_rvids).difference(baseline_rvids)

    new_ids_df = pd.DataFrame(columns=['SUBJECT_NUMBER', 'openneuro_id'])
    rowidx = 0
    for rvid in follow_up_rvids:
        onid = id_map_df.loc[id_map_df['SUBJECT_NUMBER'] == rvid, 'openneuro_id'].values[0]
        new_ids_df.at[rowidx, 'SUBJECT_NUMBER'] = rvid
        new_ids_df.at[rowidx, 'openneuro_id'] = onid
        rowidx += 1

    new_ids_df.to_csv(Path('../data/lists/new_participants_post_release_1.csv'), index=False)
