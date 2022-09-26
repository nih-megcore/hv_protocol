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

    parser.add_argument('-logdir', action='store', dest='logdir',
                        help='Directory path where log files and other metadata are stored.')

    args = parser.parse_args()
    return Path(args.input), Path(args.output), Path(args.logdir)


def run_command(cmdstr):
    p = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                         encoding='utf8', shell=True)

    return p.stdout.readline().strip()


def write_cmds_to_file(cmds_list, filepath):
    with open(filepath, 'w') as f:
        for c in cmds_list:
            f.write(c)


def deface(output_dir, modality, scans_list):
    cmds_list = []
    for scan in scans_list:
        print(scan, type(scan))
        entities = scan.name.split('_')
        acq = [i.split('-')[1] for i in entities if i.startswith('acq-')]
        if acq:
            subj_outdir = output_dir.joinpath(entities[0], entities[1], modality, acq[0])
        else:
            subj_outdir = output_dir.joinpath(entities[0], entities[1], modality)

        # filename without the extensions
        prefix = scan.name.split('.')[0]

        # make output directories within subject directory for afni
        mkdir_cmds = f"mkdir -p {subj_outdir}"

        # afni commands
        refacer = f"@afni_refacer_run -input {scan} -mode_deface -no_clean -prefix {fspath(subj_outdir.joinpath(prefix))}"

        full_cmd = ' ; '.join(
            ["START=`date +%s`", mkdir_cmds, refacer, "STOP=`date +%s`", "RUNTIME=$((STOP-START))",
             "echo ${RUNTIME}"]) + '\n'

        cmds_list.append(full_cmd)

    return cmds_list


def preprocess_facemask(fmask_path):
    prefix = fmask_path.parent.joinpath('afni_facemask')
    defacemask = fmask_path.parent.joinpath('afni_defacemask.nii.gz')

    # split the 4D volume
    c1 = f"fslroi {fmask_path} {prefix} 1 1"

    # arithmetic on the result from above
    c2 = f"fslmaths {prefix}.nii.gz -abs -binv {defacemask}"
    print(f"Splitting the facemask volume at {fmask_path} and binarizing the resulting volume... \n "
          f"{run_command('; '.join([c1, c2]))}")
    if defacemask.exists():
        return defacemask
    else:
        return f"Cannot find the binarized facemask. Please check your commands."


def find_primary_t1(t1s_list, criterion_list):
    required_t1 = None
    for t1 in t1s_list:
        t1_entities = t1.name.split('_')
        for entity in t1_entities:
            if entity in criterion_list:
                required_t1 = t1
                return required_t1


def find_scans(subj_sess_paths_dict):
    """
    Find all the T1w and corresponding non-T1w scans for each
    subject and session.

    :parameter subjs: Dictionary of paths to subject bids directories

    :return paths_dict: Nested default dictionary with T1s and
    their associated non-T1w scans' info.
    """
    paths_dict = defaultdict(lambda: defaultdict(dict))
    t1_not_found = []
    for subjid, scans_list in subj_sess_paths_dict.items():
        sess = scans_list[0].name.split('_')[1]
        t1_suffix = ('T1w.nii.gz', 'T1w.nii')
        t1s = [s for s in scans_list if s.name.endswith(t1_suffix)]
        possible_primaries = sorted([t1 for t1 in t1s if 'sourcedata' not in t1.parts])
        if not possible_primaries:
            t1_not_found.append(subjid)
            primary_t1 = "n/a"
        else:
            primary_t1_acq_labels = ('acq-FSPGR', 'acq-MPRAGE', 'acq-SagittalMPRAGE')
            primary_t1 = possible_primaries[0]
        paths_dict[subjid][sess][primary_t1] = [s for s in scans_list if s != primary_t1]
    return paths_dict, t1_not_found


def main():
    # get command line arguments
    input, output, logdir = get_args()

    # track missing files and directories
    missing = dict()

    # generate a t1 to other scans mapping
    subj_sess_paths = list(input.glob('sub-*/ses-*')) + list(input.glob('sourcedata/sub-*/ses-*'))
    subj_sess_paths_dict = defaultdict(list)
    for subj_sess_path in subj_sess_paths:
        subjid = subj_sess_path.parent.name
        subj_sess_paths_dict[subjid].extend(list(subj_sess_path.glob('anat/*nii*')))

    mapping_dict, missing_t1s = find_scans(subj_sess_paths_dict)

    # list
    t1_list = [k2 for i in mapping_dict.keys() for k1, v1 in mapping_dict[i].items()
               for k2, v2 in mapping_dict[i][k1].items() if k2 != "n/a"]
    print(len(t1_list))

    # write defacing commands to a swarm file
    defacing_cmds = deface(output, 'anat', t1_list)
    write_cmds_to_file(defacing_cmds, logdir.joinpath(f'defacing_commands_{input.name}.swarm'))

    # writing missing info to file
    missing["T1w scans"] = missing_t1s
    with open(logdir.joinpath('subj_sess_missing_t1s.json'), 'w') as f:
        json.dump(missing, f, indent=4)

    # writing mapping_dict to file
    human_readable_mapping_dict = defaultdict(lambda: defaultdict(dict))

    for subjid, _ in mapping_dict.items():
        for sess, scans in mapping_dict[subjid].items():
            for t1, others in mapping_dict[subjid][sess].items():
                if t1 != "n/a":
                    human_readable_mapping_dict[subjid][sess]["primary_t1"] = str(t1)
                    human_readable_mapping_dict[subjid][sess]["other_scans"] = [str(other) for other in others]
    # print(human_readable_mapping_dict)
    with open(logdir.joinpath('t1s_to_others_mapping.json'), 'w') as map_f:
        json.dump(human_readable_mapping_dict, map_f, indent=4)


if __name__ == "__main__":
    main()
