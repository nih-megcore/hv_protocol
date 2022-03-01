# heuristic file for Rvol dataset to be uploaded on Open Neuro

import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # anat
    t1w_mprage = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-mprage_run-{item:02d}_T1w')
    t1w_fspgr = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-fspgr_run-{item:02d}_T1w')
    t1w_fse = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-fse_run-{item:02d}_T1w')

    ## hippo
    hippo = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-highreshippo_run-{item:02d}_T1w')

    # flair 
    flair = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-t2_run-{item:02d}_FLAIR')

    ## 2d 
    flair_2d_adni = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-adni2d_run-{item:02d}_FLAIR')
    flair_2d = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-2d_run-{item:02d}_FLAIR')

    ## 3d
    flair_3d = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-3d_run-{item:02d}_FLAIR')

    # t2w
    t2w_frfse = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-frfse_run-{item:02d}_T2w')

    cube_t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-cube_run-{item:02d}_T2w')
    cube_t2_abcd = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-abcdcube_run-{item:02d}_T2w')

    # t2_star 
    t2_star = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T2star')

    # asl
    asl = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_run-{item:02d}_asl')

    # dwi 
    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:02d}_dwi')

    # func
    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_bold')

    # fmap
    fmap_dwi_24f_unflipped = create_key(
        'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-dwi_dir-unflipped_run-{item:02d}_epi')
    fmap_dwi_128_flipped = create_key(
        'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-dwib1000_dir-flipped_run-{item:02d}_epi')
    fmap_dwi = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-dwi_run-{item:02d}_fieldmap')
    fmap_func = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-resting_run-{item:02d}_fieldmap')
    rest_flip = create_key(
        'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-resting_dir-flipped_run-{item:02d}_epi')
    rest_flip_realtime = create_key(
        'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-restingrealtime_dir-flipped_run-{item:02d}_epi')

    # unspecified derived 
    cbf = create_key(
        'sourcedata/unspecified/derived/sub-{subject}/{session}/sub-{subject}_{session}_run-{item:02d}_cbf')
    avdc = create_key(
        'sourcedata/unspecified/derived/sub-{subject}/{session}/sub-{subject}_{session}_run-{item:02d}_avdc')
    trace = create_key(
        'sourcedata/unspecified/derived/sub-{subject}/{session}/sub-{subject}_{session}_run-{item:02d}_trace')
    fa = create_key('sourcedata/unspecified/derived/sub-{subject}/{session}/sub-{subject}_{session}_run-{item:02d}_fa')

    # unspecified
    localizer = create_key(
        'sourcedata/unspecified/localizer/sub-{subject}/{session}/sub-{subject}_{session}_run-{item:02d}_localizer')
    calibration_scan = create_key(
        'sourcedata/unspecified/calibration/sub-{subject}/{session}/sub-{subject}_{session}_run-{item:02d}_calibration')

    info = {
        t1w_mprage: [], t1w_fspgr: [], t1w_fse: [], hippo: [],
        flair: [], flair_2d_adni: [], flair_2d: [], flair_3d: [],
        t2w_frfse: [], cube_t2: [], cube_t2_abcd: [],
        t2_star: [],
        asl: [],
        dwi: [],
        rest: [], rest_flip: [], rest_flip_realtime: [],
        fmap_dwi: [], fmap_func: [],
        cbf: [], avdc: [], trace: [], fa: [],
        localizer: [], calibration_scan: [], fmap_dwi_128_flipped: [],
        fmap_dwi_24f_unflipped: []
    }

    last_run = len(seqinfo)

    for idx, s in enumerate(seqinfo):

        # anat
        # t1w fspgr
        series_descriptors_fspgr = ['Accelerated Sagittal IR-FSPGR']
        for each in series_descriptors_fspgr:
            if each in s.series_description:
                info[t1w_fspgr].append([s.series_id])

        # t1w mprage
        series_descriptors_mprage = ['Anat T1w MP-RAGE 1mm (ABCD)', 'PURE MP-RAGE 1mm', \
                                     'Sag_MPRAGE_T1']
        for each in series_descriptors_mprage:
            if each in s.series_description:
                info[t1w_mprage].append([s.series_id])

        # t1w fse       
        series_descriptors_fse = ['Sag T1 FSE']
        for each in series_descriptors_fse:
            if each in s.series_description:
                info[t1w_fse].append([s.series_id])

        # hippo
        if 'HighResHippo' in s.series_description:
            info[hippo].append([s.series_id])

        # flair 
        series_descriptors_flair = ['Ax T2 FLAIR']
        for each in series_descriptors_flair:
            if each in s.series_description:
                info[flair].append([s.series_id])

        # 2d
        series_descriptors_flair_2d = ['Axial T2 2D FLAIR ADNI2', 'ADNI2 2D FLAIR',
                                       'Axial T2 2D FLAIR', 'Axial T2  2D FLAIR']
        for each in series_descriptors_flair_2d:
            if each in s.series_description:
                info[flair_2d].append([s.series_id])

        # 3d 
        series_descriptors_flair_3d = ['Optional - Anat T2w CUBE FLAIR', \
                                       'Optional - Sagittal 3D FLAIR', 'Sagittal 3D FLAIR']
        for each in series_descriptors_flair_3d:
            if each in s.series_description:
                info[flair_3d].append([s.series_id])

        # t2w
        series_descriptors_t2_fsfse = ['Ax T2 FRFSE']
        for each in series_descriptors_t2_fsfse:
            if each in s.series_description:
                info[t2w_frfse].append([s.series_id])

        # cube_t2
        series_descriptors_cube_t2 = ['Sag_CUBE_T2', 'Anat T2w CUBE (ABCD)']
        for each in series_descriptors_cube_t2:
            if each in s.series_description:
                info[cube_t2].append([s.series_id])

        # t2star
        series_descriptors_t2_star = ['Axial T2 Star', 'Axial T2 Star (Rx 2D FLAIR)']
        for each in series_descriptors_t2_star:
            if each in s.series_description:
                info[t2_star].append([s.series_id])

        # asl
        series_descriptors_asl = ['Axial 3D pCASL with Eyes Open', 'Axial 3D pCASL (Eyes Open)']
        for each in series_descriptors_asl:
            if each in s.series_description:
                info[asl].append([s.series_id])

        # dwi 
        series_descriptors_dwi = ['Axial DTI']
        for each in series_descriptors_dwi:
            if each in s.series_description:
                info[dwi].append([s.series_id])

        # B1000, dim1=128 and B1000, dim1=256
        series_descriptors_dwi_b1000 = ['Axial DTI B 1000', 'Axial DTI B 1000 - RKV', 'Axial DTI B=1000']
        for each in series_descriptors_dwi_b1000:
            if each in s.series_description:
                info[fmap_dwi_128_flipped].append([s.series_id])

        # 24 dirs flipped 
        series_descriptors_24f_dwi = ['Axial DTI 24dirs flipped - RKV',
                                      'Axial DTI 24dir flipped',
                                      'Axial DTI 24dirs flipped'
                                      'Axial DTI 24vols flipped']
        for each in series_descriptors_24f_dwi:
            if each in s.series_description:
                info[fmap_dwi_24f_unflipped].append([s.series_id])

        # func
        # rest & rest_rt
        series_descriptors_rest = ['Axial rsfMRI with Eyes Open - RKV', 'Axial rsfMRI (Eyes Open)']
        for each in series_descriptors_rest:
            if each in s.series_description and s.sequence_name == 'epi':
                info[rest].append([s.series_id])

        # rest flip & rest flip rt
        series_descriptors_rest_flip = ['Axial rsfMRI reverse blip - RKV', 'Axial fMRI reverse blip']
        for each in series_descriptors_rest_flip:
            if each in s.series_description and s.sequence_name == 'epi':
                info[rest_flip].append([s.series_id])

        # fmap 
        series_descriptors_fmap_dwi = ['B0 Map - DTI - RKV', 'B0 Map - DTI']
        for each in series_descriptors_fmap_dwi:
            if each in s.series_description:
                info[fmap_dwi].append([s.series_id])

        series_descriptors_fmap_func = ['B0 Map - rsfMRI - RKV', 'B0 Map - rsfMRI']
        for each in series_descriptors_fmap_func:
            if each in s.series_description:
                info[fmap_func].append([s.series_id])

        # unspecified derived     
        if s.series_description.startswith('Trace'):
            info[trace].append([s.series_id])
        if s.series_description.startswith('FA'):
            info[fa].append([s.series_id])
        if s.series_description.startswith('AvDC'):
            info[avdc].append([s.series_id])
        if s.series_description.startswith('CBF'):
            info[cbf].append([s.series_id])

            # unspecified - localizer and calibration scans
        localizer_var = ['3 Plane Localizer', '3Plane Loc SSFSE']
        for each in localizer_var:
            if each in s.series_description:
                info[localizer].append([s.series_id])

        calibration_var = ['Calibration Scan', 'Cal 32Ch Head', 'ASSET calibration']
        for each in calibration_var:
            if each in s.series_description:
                info[calibration_scan].append([s.series_id])

        # ORIG 
        if 'ORIG' in s.series_description:
            pass

    return info
