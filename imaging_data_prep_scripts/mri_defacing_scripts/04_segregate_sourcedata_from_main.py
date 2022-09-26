import argparse
import json
import subprocess
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(description="Does something worth doing.")

    parser.add_argument("-i", "--input-dir", type=Path, action='store', dest='inputdir',
                        help="Path to BIDS-like directory with defaced scans.")
    parser.add_argument("-o", "--output-dir", type=Path, action='store', dest='outdir',
                        help="Path to sourcedata directory with defaced scans.")
    parser.add_argument("-m", "--mapping-file", type=Path, action='store', dest='mapping_file',
                        help="Path afni work directory to sourcedata scans mapping file.")

    args = parser.parse_args()
    return args.inputdir, args.outdir, args.mapping_file


def run_shell_cmd(cmdstr):
    pipe = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, encoding='utf8', shell=True)
    print(pipe.stdout)


def copy_over_sourcedata_files(mapping_data, outdir):
    for afni_workdir_path, srcdata_scans in mapping_data.items():
        for scan in srcdata_scans:
            # converting from str type to Path type variable
            scan = Path(scan)
            afni_workdir_path = Path(afni_workdir_path)

            # constructing src and dest file paths for the copy command
            if not scan.name.startswith('tmp'):
                defaced_dir = scan.name.split('.')[0]
                entities = scan.name.split('_')
                subj_sess_outdir = outdir.joinpath(entities[0], entities[1], 'anat')
                src = afni_workdir_path.joinpath(defaced_dir, defaced_dir + '_defaced.nii.gz')  # path to defaced image
                dest = subj_sess_outdir.joinpath(defaced_dir + '.nii.gz')
            else:
                scan_name_entities = afni_workdir_path.name.split('_')  # first element of this list will be "workdir"
                subj_sess_outdir = outdir.joinpath(scan_name_entities[1], scan_name_entities[2], 'anat')
                src = afni_workdir_path.joinpath(scan.name)  # path to defaced image
                dest = subj_sess_outdir.joinpath('_'.join(scan_name_entities[1:]) + '.nii.gz')

            if not dest.parent.exists():
                dest.parent.mkdir(parents=True)  # make destination directory if it doesn't already exist
            cp_cmd = f"cp {src} {dest} ;"
            run_shell_cmd(cp_cmd)


def main():
    inputdir, outdir, mapping_file = parse_arguments()

    # load sourcedata mapping file as a dictionary
    f = open(mapping_file, 'r')
    mapping_data = json.load(f)

    for scan_location, _ in mapping_data.items():
        for afni_workdir_path, scans_list in mapping_data[scan_location].items():
            for scan in scans_list:
                # converting from str type to Path type variable
                scan = Path(scan)
                afni_workdir_path = Path(afni_workdir_path)

                # constructing src and dest file paths for the copy command
                if not scan.name.startswith('tmp'):
                    defaced_dir = scan.name.split('.')[0]
                    entities = scan.name.split('_')
                    if scan_location == "sourcedata":
                        subj_sess_outdir = outdir.joinpath('sourcedata', 'auxiliary_scans', entities[0], entities[1],
                                                           'anat')
                    else:
                        subj_sess_outdir = outdir.joinpath(entities[0], entities[1], 'anat')

                    src = afni_workdir_path.joinpath(defaced_dir,
                                                     defaced_dir + '_defaced.nii.gz')  # path to defaced image
                    dest = subj_sess_outdir.joinpath(defaced_dir + '.nii.gz')  # path in bids tree with defaced images
                else:
                    # first element of this list will be "workdir"
                    scan_name_entities = afni_workdir_path.name.split('_')
                    if scan_location == "sourcedata":
                        subj_sess_outdir = outdir.joinpath('sourcedata', 'auxiliary_scans', scan_name_entities[1],
                                                           scan_name_entities[2],
                                                           'anat')
                    else:
                        subj_sess_outdir = outdir.joinpath(scan_name_entities[1], scan_name_entities[2], 'anat')
                    src = afni_workdir_path.joinpath(scan.name)  # path to defaced image
                    dest = subj_sess_outdir.joinpath('_'.join(scan_name_entities[1:]) + '.nii')

                if not dest.parent.exists():
                    dest.parent.mkdir(parents=True)  # make destination directory if it doesn't already exist
                cp_cmd = f"cp {src} {dest} ;"
                run_shell_cmd(cp_cmd)


if __name__ == "__main__":
    main()
