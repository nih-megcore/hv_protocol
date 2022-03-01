
## Instructions to generate outputs

Code used to generate the phenotype files in BIDS format.

To generate a new set of outputs, please follow the instructions below -

1. Run `python 01_cris_clean_up.py` from `/data/rvol/arsh_workspace/code`
2. Edit cris tsvs manually using cris_manual_edits.md as ref
    - go over each tsv and remove rows with majority responses as "SEE NOTE"
        - `sub-ON87555` in `acute_care.tsv`, `hepatic.tsv`
    - replace "SEE NOTE" for `sub-ON99871` to -999 in `cbc_with_differential.tsv`
    - verify if
        - "< " are replaced with "<"
        - text like "Hemolyzed" are all capitalized
        - trailing zeros from field names are removed
3. Run `python 02_ctdb_clean_up.py` from `/data/rvol/arsh_workspace/code`
4. Run `python 03_post_conversion_edits.py` from `/data/rvol/arsh_workspace/code`
5. Edit ctdb tsvs manually using ctdb_manual_edits.md as ref
6. Run `python 04_generate_bids_phenotype_tree.py` from `/data/rvol/arsh_workspace/code`
7. Run `python 05_generate_participants_tsv.py` 
8. Run `hv_proc/utilities/fix_jsons.py` to add the fiducial locations to the run1_T1w.json anatomical file in voxel index
