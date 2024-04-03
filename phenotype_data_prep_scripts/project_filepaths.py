from pathlib import Path
import time

work_dir = Path('/Users/arshithab/Desktop/Projects/rvol/release_2/phenotype')


def generate_new_outputs_dir():
    timestr = time.strftime('%Y%m%d')  # outputs generated
    new_outdir = work_dir.joinpath('outputs_' + timestr)
    new_outdir.joinpath('bids_ctdb').mkdir(parents=True, exist_ok=True)
    new_outdir.joinpath('bids_cris').mkdir(parents=True, exist_ok=True)
    return new_outdir


data_dir = work_dir.joinpath('data')
id_filepath = data_dir.joinpath('id_files', 'id_linking_file_20240402_171021.csv')

# cris and ctdb data directories
cris_data_dir = data_dir.joinpath('cris_downloads', '17-M-0181_CRIS_Labs_FINAL.xls')
ctdb_data_dir = data_dir.joinpath('ctdb_downloads', 'CTDBDataDownload_20240401.xlsx')
ctdb_legends_dir = data_dir.joinpath('ctdb_downloads', 'CTDB_form_legend.xlsx')

# cris and ctdb output directories
curr_outputs_dir = generate_new_outputs_dir()
cris_out_dir = Path(curr_outputs_dir, 'bids_cris')
ctdb_out_dir = Path(curr_outputs_dir, 'bids_ctdb')

# mapping files
free_text_list = data_dir.joinpath('mappings', 'ctdb_form_exclusions.txt')
