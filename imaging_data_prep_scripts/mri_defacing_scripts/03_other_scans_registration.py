import argparse
import json
import subprocess
from collections import defaultdict
from os import fspath
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate a swarm command file to deface T1w scans for a given BIDS dataset.')

    parser.add_argument('-in', action='store', dest='input',
                        help='Path to input BIDS dataset.')

    parser.add_argument('-out', action='store', dest='output',
                        help='Path to output dataset.')

    parser.add_argument('-m', '--mapping-file', action='store', dest='map',
                        help='JSON file with mapping of primary to other scans.')

    parser.add_argument('-s', '--script-output-files', action='store', dest='logdir',
                        help='Directory path where log files and other metadata are stored.')

    args = parser.parse_args()
    return Path(args.input), Path(args.output), Path(args.map), Path(args.logdir)


def run_command(cmdstr):
    p = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                         encoding='utf8', shell=True)

    return p.stdout.readline().strip()


def write_cmds_to_file(cmds_list, filepath):
    with open(filepath, 'w') as f:
        for c in cmds_list:
            f.write(c)


def preprocess_facemask(fmask_path):
    prefix = fmask_path.parent.joinpath('afni_facemask')
    defacemask = fmask_path.parent.joinpath('afni_defacemask.nii.gz')

    # load fsl module
    c0 = f"module load fsl"

    # split the 4D volume
    c1 = f"fslroi {fmask_path} {prefix} 1 1"

    # arithmetic on the result from above
    c2 = f"fslmaths {prefix}.nii.gz -abs -binv {defacemask}"
    print(f"Splitting the facemask volume at {fmask_path} and binarizing the resulting volume... \n "
          f"{run_command('; '.join([c0, c1, c2]))}")
    try:
        if defacemask.exists():
            return defacemask
    except OSError as err:
        print(f"OS Error: {err}")
        print(
            f"Cannot find the binarized facemask. Please check is fsl module is loaded before running the script again.")
        raise


def registration(input_dir, output_dir, t1_list, scans_dict):
    sourcedata_maindata_mapping_dict = defaultdict(lambda: defaultdict(list))
    # main_data_mapping_dict = defaultdict(list)
    afni_workdir_not_found = []
    cmds = []
    modality = 'anat'
    for t1 in t1_list:
        entities = t1.name.split('_')
        subjid = entities[0]  # subjid
        sess = entities[1]  # sess id
        others = scans_dict[subjid][sess]["other_scans"]
        acq = [i.split('-')[1] for i in entities if i.startswith('acq-')]
        if acq:
            subj_outdir = output_dir.joinpath(entities[0], entities[1], modality, acq[0])
        else:
            subj_outdir = output_dir.joinpath(entities[0], entities[1], modality)

        # make output directories within subject directory for fsl flirt
        afni_workdir = list(subj_outdir.glob('work*'))

        if not afni_workdir:
            afni_workdir_not_found.append(t1.name)
        else:
            afni_workdir = afni_workdir[0]

            # separate out sourcedata primary t1s from main data t1s, and create mapping files for each
            afni_workdir_suffix = afni_workdir.name.split('workdir_')[1]
            if "sourcedata" in t1.parts:
                # converting Path to str coz Path type is not JSON serializable
                if t1.name.split('.')[0] == afni_workdir_suffix:
                    sourcedata_maindata_mapping_dict['sourcedata'][str(afni_workdir)].append(
                        str(t1.parent.joinpath('tmp.99.result.deface.nii')))
                else:
                    sourcedata_maindata_mapping_dict[['sourcedata']][str(afni_workdir)].append(str(t1))
            else:
                if t1.name.split('.')[0] == afni_workdir_suffix:
                    sourcedata_maindata_mapping_dict['main'][str(afni_workdir)].append(
                        str(t1.parent.joinpath('tmp.99.result.deface.nii')))
                else:
                    sourcedata_maindata_mapping_dict['main'][str(afni_workdir)].append(str(t1))

            # preprocess facemask
            raw_facemask_volumes = afni_workdir.joinpath('tmp.05.sh_t2a_thr.nii')
            t1_mask = preprocess_facemask(raw_facemask_volumes)
            # print(t1_mask)
            for other in others:
                entities = other.split('_')

                # separate out sourcedata "other" scans from main data "other" scans, and create mapping files for each
                if "sourcedata" in Path(other).parts:
                    # converting Path to str coz Path type is not JSON serializable
                    sourcedata_maindata_mapping_dict['sourcedata'][str(afni_workdir)].append(str(other))
                else:
                    sourcedata_maindata_mapping_dict['main'][str(afni_workdir)].append(str(other))

                # changing other scan name to other scan full path
                other = input_dir.joinpath(entities[0], entities[1], modality, other)
                other_prefix = other.name.split('.')[0]
                other_outdir = afni_workdir.joinpath(other_prefix)

                matrix = f"{other_outdir.joinpath(other_prefix)}_reg.mat"
                out = f"{other_outdir.joinpath('registered.nii.gz')}"
                other_mask = f"{other_outdir.joinpath(other_prefix)}_mask.nii.gz"
                other_defaced = f"{other_outdir.joinpath(other_prefix)}_defaced.nii.gz"

                mkdir_cmd = f"mkdir -p {other_outdir}; cp {other} {other_outdir.joinpath('original.nii.gz')}"

                flirt_cmd = f"flirt -dof 6 -cost mutualinfo -searchcost mutualinfo -in {t1} " \
                            f"-ref {other} -omat {matrix} -out {out}"

                # t1 mask can be found in the afni work directory
                applyxfm_cmd = f"flirt -interp nearestneighbour -applyxfm -init {matrix} " \
                               f"-in {t1_mask} -ref {other} -out {other_mask}"

                mask_cmd = f"fslmaths {other} -mas {other_mask} {other_defaced}"
                full_cmd = " ; ".join([mkdir_cmd, flirt_cmd, applyxfm_cmd, mask_cmd]) + '\n'
                print(full_cmd)
                cmds.append(full_cmd)

    return cmds, afni_workdir_not_found, sourcedata_maindata_mapping_dict


def main():
    # get command line arguments
    input, output, map, logdir = get_args()

    # track missing files and directories
    f = open(fspath(map), 'r')
    mapping_dict = json.load(f)

    # list of primary t1s
    primary_list = [input.joinpath(subjid, sess, 'anat', v2) for subjid in mapping_dict.keys() for sess, v1 in
                    mapping_dict[subjid].items() for k2, v2 in mapping_dict[subjid][sess].items() if
                    k2 == "primary_t1"]

    # write registration commands to a swarm file
    registration_cmds, missing_afni_wrkdirs, sourcedata_maindata_mapping_dict = registration(input, output,
                                                                                             primary_list,
                                                                                             mapping_dict)
    write_cmds_to_file(registration_cmds, logdir.joinpath(f'registration_commands_{input.name}.swarm'))

    # write sourcedata files mapping to json file
    with open(logdir.joinpath('sourcedata_maindata_files_mapping.json'), 'w') as m:
        json.dump(sourcedata_maindata_mapping_dict, m, indent=4)

    # writing missing info to file
    missing = dict()
    missing["afni workdirs"] = missing_afni_wrkdirs
    with open(logdir.joinpath('missing_afni_workdirs.json'), 'w') as f:
        json.dump(missing, f, indent=4)


if __name__ == "__main__":
    main()
