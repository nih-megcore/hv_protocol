"""
Installation
If you don't already have `pydeface` installed then you can find the instructions to do so
[here](https://github.com/poldracklab/pydeface). Running `pydeface --help`,
after successful installation, is the most documentation available as of March 24th, 2021.

Modified `pydeface` workflow for HV-Protocol dataset

PART 1: 
1. `fslmaths facemask.nii.gz -binv facemask_inv` (inverting default facemask)
2. `pydeface sub-ON01802_ses-01_acq-mprage_run-01_T1w.nii.gz --facemask ../../pydeface-defaults/data/facemask-inv.nii.gz --nocleanup --verbose --debug > T1w-deface-facemask-inv.txt`
3. `fslmaths sub-ON01802_ses-01_acq-mprage_run-01_T1w_pydeface_mask.nii.gz -binv inverted-T1w-pydeface-mask`
4. `fslmaths inverted-T1w-pydeface-mask.nii.gz -mul sub-ON01802_ses-01_acq-mprage_run-01_T1w.nii.gz sub-ON01802_ses-01_acq-mprage_run-01_T1w-new-mask-defaced.nii.gz`

PART 2: 
a. FLAIR 
- `pydeface sub-ON01802_ses-01_acq-2d_run-01_FLAIR.nii.gz --template sub-ON01802_ses-01_acq-mprage_run-01_T1w.nii.gz --facemask inverted-T1w-pydeface-mask.nii.gz --nocleanup --verbose --force --debug > flair_pydeface.txt`
- `fslmaths sub-ON01802_ses-01_acq-2d_run-01_FLAIR_pydeface_mask.nii.gz -binv inverted-flair-pydeface-mask`
- `fslmaths inverted-flair-pydeface-mask -mul sub-ON01802_ses-01_acq-2d_run-01_FLAIR.nii.gz sub-ON01802_ses-01_acq-2d_run-01_FLAIR_new-mask-defaced.nii.gz` 

b. T2w 
- `pydeface sub-ON01802_ses-01_acq-abcdcube_run-01_T2w.nii.gz --template sub-ON01802_ses-01_acq-mprage_run-01_T1w.nii.gz --facemask inverted-T1w-pydeface-mask.nii.gz --nocleanup --verbose --force --debug > T2w-deface-facemask-inv.txt`
- `fslmaths sub-ON01802_ses-01_acq-abcdcube_run-01_T2w_pydeface_mask.nii.gz -binv inverted-T2w-pydeface-mask`
- `fslmaths inverted-T2w-pydeface-mask -mul sub-ON01802_ses-01_acq-abcdcube_run-01_T2w.nii.gz sub-ON01802_ses-01_acq-abcdcube_run-01_T2w_new-mask-defaced.nii.gz`

c. T2star
- `pydeface sub-ON01802_ses-01_run-01_T2star.nii.gz --template sub-ON01802_ses-01_acq-mprage_run-01_T1w.nii.gz --facemask inverted-T1w-pydeface-mask.nii.gz --nocleanup --verbose --force --debug > T2star-deface-facemask-inv.txt`
- `fslmaths sub-ON01802_ses-01_run-01_T2star_pydeface_mask.nii.gz -binv inverted-T2star-pydeface-mask`
- `fslmaths inverted-T2star-pydeface-mask -mul sub-ON01802_ses-01_run-01_T2star.nii.gz sub-ON01802_ses-01_run-01_T2star_new-mask-defaced.nii.gz`

"""
import os
from pathlib import Path


def check_job_status(user):
    log = get_ipython().getoutput('squeue -u $user')
    if log:
        for each in log:
            print(each)


if __name__ == "__main__":
    data_path = Path(
        "/data/BrainBlocks/joyce/bids_modified/missing_toshare_raw_data")  # directory path that contains subject data

    # the nodeface-anat-scans directory contains a COPY of all the anat scans in the dataset.
    # No directories, just a bunch of anat scans all in one place, for example -
    anat_scans_with_face = data_path.joinpath("derivatives", "nodeface-anat-scans")
    listing = os.listdir(anat_scans_with_face)

    # create an output directory to store the pydeface outputs in. Within the output directory, one directory per
    # subject would make life easier while merging defaced scans with original directory tree that contains anat
    # scans with faces
    output_dir = data_path.joinpath("derivatives", "pydeface_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Command to Inverting default facemask using the fslmaths command
    inv_facemask_path = data_path.joinpath('derivatives', 'inverted_default_facemask.nii.gz')
    inv_cmd = f"fslmaths {data_path.joinpath('derivatives', 'pydeface_defaults', 'facemask.nii.gz')} -binv {inv_facemask_path}"
    print(inv_cmd)

    # bids tree that contains anat scans with face (NOT the same as the nodeface-anat-scans under derivatives)
    bids_root = data_path

    # list of subject directories in the dataset
    subjects = [subj for subj in os.listdir(bids_root) if subj.startswith("sub-") and not subj.endswith("emptyroom")]
    scans_with_face = [x for x in os.listdir(anat_scans_with_face) if x.endswith(".nii.gz")]

    for subj in subjects:
        subj_anat_scans = [os.path.join(anat_scans_with_face, file) for file in os.listdir(anat_scans_with_face)
                           if file.startswith(subj) and file.endswith(".nii.gz")]
        # uncomment the next line if you'd like to see the list generated above
        # print(subj_anat_scans)
        for scan in subj_anat_scans:
            # create a subj directory within output directory
            subj_outdir = output_dir.joinpath(subj)
            subj_outdir.mkdir(parents=True, exist_ok=True)

        # construct pydeface commands for each subject
        # using lscratch for computations can be faster too
        # hence, the TMPDIR installations
        env_variables = " ".join(["source ~/.bashrc;",
                                  "export TMPDIR=/lscratch/$SLURM_JOB_ID;",
                                  "mkdir $TMPDIR/bids;", "mkdir $TMPDIR/out;",
                                  "cp", " ".join(subj_anat_scans), "$TMPDIR/bids;",
                                  "conda activate base", ";"
                                  # this'll work only if the .bashrc/.bash_profile initializes conda
                                  ])
        tmp_input_dir = "$TMPDIR/bids"
        tmp_output_dir = "$TMPDIR/out"

        # copying the default inverted facemask to working directory
        cp_default_inv_facemask = f"cp {inv_facemask_path} {tmp_input_dir};"

        # the T1w image for each subject being set as the template image for non-T1w modalities
        template_image = Path([image for image in subj_anat_scans if image.endswith("_T1w.nii.gz")][0])

        # defacing the template image using the inverted default facemask
        template_deface_cmd = f"pydeface {os.path.join(tmp_input_dir, template_image.name)} " \
                              f"--facemask {os.path.join(tmp_input_dir, inv_facemask_path.name)} " \
                              f"--nocleanup " \
                              f"--verbose --force " \
                              f"--outfile " \
                              f"{os.path.join(tmp_output_dir, template_image.name.split('.')[0] + '_inv_defaced.nii.gz')};"

        # setting the path to the subject specific template facemask
        template_facemask_path = os.path.join(tmp_output_dir, "T1w-facemask.nii.gz")

        # creates a inverted defaced image of the T1w image
        # inverting the inverted defaced image of the T1w scan
        # would create the final defaced T1w image
        fslmath_cmds = ' '.join(["fslmaths", os.path.join(tmp_input_dir, "*T1w_pydeface_mask*"),
                                 "-binv", template_facemask_path, ";",
                                 "fslmaths", os.path.join(tmp_input_dir, template_image.name),
                                 "-mul", template_facemask_path,
                                 os.path.join(tmp_output_dir, template_image.name.split('.')[0] + "_defaced.nii.gz"),
                                 ";"])

        # the following commands are meant to deface the non-T1w scans
        non_T1w_cmds = ""
        for image in subj_anat_scans:
            # print(image)
            if image != template_image and not image.endswith("_pydeface_mask.nii.gz"):
                image = Path(image)
                non_T1w_cmds = " ".join([non_T1w_cmds, "pydeface", os.path.join(tmp_input_dir, image.name),
                                         "--template", os.path.join(tmp_input_dir, template_image.name),
                                         "--facemask", template_facemask_path,
                                         "--nocleanup", "--verbose", "--force",
                                         "--outfile",
                                         os.path.join(tmp_output_dir, image.name.split('.')[0] + "_defaced.nii.gz"),
                                         ";"])

        mv_pydeface_tmp_cmd = ' '.join(["mv", os.path.join(tmp_input_dir, "*_pydeface*"),
                                        tmp_output_dir, ";"])

        mv_tmp_out_dir = " ".join(["mv", os.path.join(tmp_output_dir, "*"), subj_outdir.as_posix(), ";"])
        chng_perms = " ".join(["chmod -R ug+rwx", subj_outdir.as_posix(), ";"])
        rm_tmp_dirs = " ".join(["rm -rf", tmp_input_dir, tmp_output_dir, ";"])
        print(' '.join([env_variables, cp_default_inv_facemask, '\n', template_deface_cmd, '\n', fslmath_cmds, '\n',
                        non_T1w_cmds, '\n', mv_pydeface_tmp_cmd, mv_tmp_out_dir,
                        chng_perms, rm_tmp_dirs, '\n']))
        print('==================================================================================================')

    # Once you create the swarm command file from above, the next step would be to run it on the biowulf command line.
    # ********* TO BE CHANGED TO SET SWARM JOB RESOURCES *********#
    swarm_filepath = str(bids_root.joinpath("code", 'pydeface-cmds.swarm'))
    logdir = str(bids_root.joinpath("code", "swarm_log"))
    threads = str(8)
    memory = str(32)
    wall_time = "48:00:00"
    jobname = "pydeface"
    module = "fsl"
    lscratch = str(50)
    bundle = str(0)

    cmd = f"swarm -f {swarm_filepath} --gres=lscratch:{lscratch} -g {memory} -t {threads} -b {bundle} " \
          f"--logdir {logdir} --time {wall_time} --job-name {jobname} --module {module}"

    biowulf_username = "arshithab"

    check_job_status(biowulf_username)
