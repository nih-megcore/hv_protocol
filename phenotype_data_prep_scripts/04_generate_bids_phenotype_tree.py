import shutil
from pathlib import Path

import project_filepaths as filepaths

phenotype_bids_path = filepaths.work_dir.joinpath('bids_phenotype')
if not phenotype_bids_path.exists():
    Path.mkdir(phenotype_bids_path / 'phenotype', parents=True, exist_ok=True)

modality_agnostic_files = filepaths.work_dir.joinpath('../eric_workspace/repo/modality_agnostics')
required_files = ['CHANGES', 'dataset_description.json', 'LICENSE', 'participants.json']
for f in modality_agnostic_files.iterdir():
    if f.name in required_files:
        shutil.copy2(modality_agnostic_files.joinpath(f), phenotype_bids_path)

# copy over cris files
for p in list(filepaths.cris_out_dir.glob('*')):
    shutil.copy2(p, phenotype_bids_path.joinpath('phenotype'))

# copy over ctdb files
for p in list(filepaths.ctdb_out_dir.glob('*')):
    shutil.copy2(p, phenotype_bids_path.joinpath('phenotype'))
