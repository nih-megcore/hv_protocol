[![DOI](https://zenodo.org/badge/464975691.svg)](https://zenodo.org/badge/latestdoi/464975691)

# The NIMH Healthy Research Volunteer Dataset

A comprehensive clinical, MRI, and MEG collection characterizing healthy research volunteers collected at the National Institute of Mental Health (NIMH) Intramural Research Program (IRP) in Bethesda, Maryland using medical and mental health assessments, diagnostic and dimensional measures of mental health, cognitive and neuropsychological functioning, structural and functional magnetic resonance imaging (MRI), along with diffusion tensor imaging (DTI), and a comprehensive magnetoencephalography battery (MEG).

In addition, blood samples are currently banked for future genetic analysis. All data collected in this protocol are broadly shared in the OpenNeuro repository, in the Brain Imaging Data Structure (BIDS) format. In addition, blood samples of healthy volunteers are banked for future analyses. All data collected in this protocol are broadly shared here, in the Brain Imaging Data Structure (BIDS) format. In addition, task paradigms and basic pre-processing scripts are shared on GitHub. This dataset is unique in its depth of characterization of a healthy population in terms of brain health and will contribute to a wide array of secondary investigations of non-clinical and clinical research questions.

This dataset is licensed under the [Creative Commons Zero (CC0) v1.0 License](https://creativecommons.org/publicdomain/zero/1.0/).

## Recruitment

Inclusion criteria for the study require that participants are adults at or over 18 years of age in good health with the ability to read, speak, understand, and provide consent in English. All participants provided electronic informed consent for online screening and written informed consent for all other procedures. Exclusion criteria include:

- A history of significant or unstable medical or mental health condition requiring treatment
- Current self-injury, suicidal thoughts or behavior
- Current illicit drug use by history or urine drug screen
- Abnormal physical exam or laboratory result at the time of in-person assessment
- Less than an 8th grade education or IQ below 70
- Current employees, or first-degree relatives of NIMH employees

Study participants are recruited through direct mailings, bulletin boards and listservs, outreach exhibits, print advertisements, and electronic media.

## Clinical Measures

All potential volunteers first visit the study website ([https://nimhresearchvolunteer.ctss.nih.gov](https://nimhresearchvolunteer.ctss.nih.gov)), check a box indicating consent, and complete preliminary self-report screening questionnaires. The study website is HIPAA compliant and therefore does not collect PII ; instead, participants are instructed to contact the study team to provide their identity and contact information. The questionnaires include demographics, clinical history including medications, disability status (WHODAS 2.0), mental health symptoms (modified DSM-5 Self-Rated Level 1 Cross-Cutting Symptom Measure), substance use survey (DSM-5 Level 2), alcohol use (AUDIT), handedness (Edinburgh Handedness Inventory), and perceived health ratings. At the conclusion of the questionnaires, participants are again prompted to send an email to the study team. Survey results, supplemented by NIH medical records review (if present), are reviewed by the study team, who determine if the participant is likely eligible for the protocol. These participants are then scheduled for an in-person assessment. Follow-up phone screenings were also used to determine if participants were eligible for in-person screening.

## In-person Assessments

At this visit, participants undergo a comprehensive clinical evaluation to determine final eligibility to be included as a healthy research volunteer. The mental health evaluation consists of a psychiatric diagnostic interview (Structured Clinical Interview for DSM-5 Disorders (SCID-5), along with self-report surveys of mood (Beck Depression Inventory-II (BD-II) and anxiety (Beck Anxiety Inventory, BAI) symptoms. An intelligence quotient (IQ) estimation is determined with the Kaufman Brief Intelligence Test, Second Edition (KBIT-2). The KBIT-2 is a brief (20-30 minute) assessment of intellectual functioning administered by a trained examiner. There are three subtests, including verbal knowledge, riddles, and matrices.

## Medical Evaluation

Medical evaluation includes medical history elicitation and systematic review of systems. Biological and physiological measures include vital signs (blood pressure, pulse), as well as weight, height, and BMI. Blood and urine samples are taken and a complete blood count, acute care panel, hepatic panel, thyroid stimulating hormone, viral markers (HCV, HBV, HIV), C-reactive protein, creatine kinase, urine drug screen and urine pregnancy tests are performed. In addition, blood samples that can be used for future genomic analysis, development of lymphoblastic cell lines or other biomarker measures are collected and banked with the NIMH Repository and Genomics Resource (Infinity BiologiX). The Family Interview for Genetic Studies (FIGS) was later added to the assessment in order to provide better pedigree information; the Adverse Childhood Events (ACEs) survey was also added to better characterize potential risk factors for psychopathology. The entirety of the in-person assessment not only collects information relevant for eligibility determination, but it also provides a comprehensive set of standardized clinical measures of volunteer health that can be used for secondary research.

## MRI Scan

Participants are given the option to consent for a magnetic resonance imaging (MRI) scan, which can serve as a baseline clinical scan to determine normative brain structure, and also as a research scan with the addition of functional sequences (resting state and diffusion tensor imaging). The MR protocol used was initially based on the ADNI-3 basic protocol, but was later modified to include portions of the ABCD protocol in the following manner:

1. The T1 scan from ADNI3 was replaced by the T1 scan from the ABCD protocol.
2. The Axial T2 2D FLAIR acquisition from ADNI2 was added, and fat saturation turned on.
3. Fat saturation was turned on for the pCASL acquisition.
4. The high-resolution in-plane hippocampal 2D T2 scan was removed and replaced with the whole brain 3D T2 scan from the ABCD protocol (which is resolution and bandwidth matched to the T1 scan).
5. The slice-select gradient reversal method was turned on for DTI acquisition, and reconstruction interpolation turned off.
6. Scans for distortion correction were added (reversed-blip scans for DTI and resting state scans).
7. The 3D FLAIR sequence was made optional and replaced by one where the prescription and other acquisition parameters provide resolution and geometric correspondence between the T1 and T2 scans.

At the time of the MRI scan, volunteers are administered a subset of tasks from the NIH Toolbox Cognition Battery. The four tasks include:

1. Flanker inhibitory control and attention task assesses the constructs of attention and executive functioning.
2. Executive functioning is also assessed using a dimensional change card sort test.
3. Episodic memory is evaluated using a picture sequence memory test.
4. Working memory is evaluated using a list sorting test.

## MEG

An optional MEG study was added to the protocol approximately one year after the study was initiated, thus there are relatively fewer MEG recordings in comparison to the MRI dataset. MEG studies are performed on a 275 channel CTF MEG system (CTF MEG, Coquiltam BC, Canada). The position of the head was localized at the beginning and end of each recording using three fiducial coils. These coils were placed 1.5 cm above the nasion, and at each ear, 1.5 cm from the tragus on a line between the tragus and the outer canthus of the eye. For 48 participants (as of 2/1/2022), photographs were taken of the three coils and used to mark the points on the T1 weighted structural MRI scan for co-registration. For the remainder of the participants (n=16 as of 2/1/2022), a Brainsight neuronavigation system (Rogue Research, Montr??al, Qu??bec, Canada) was used to coregister the MRI and fiducial localizer coils in realtime prior to MEG data acquisition.

## Specific Measures within Dataset

Online and In-person behavioral and clinical measures, along with the corresponding phenotype file name, sorted first by measurement location and then by file name.

| Location  | Measure                                                                                         | File Name                |
| --------- | ----------------------------------------------------------------------------------------------- | ------------------------ |
| Online    | Alcohol Use Disorders Identification Test (AUDIT)                                               | audit                    |
|           | Demographics                                                                                    | demographics             |
|           | DSM-5 Level 2 Substance Use - Adult                                                             | drug_use                 |
|           | Edinburgh Handedness Inventory (EHI)                                                            | ehi                      |
|           | Health History Form                                                                             | health_history_questions |
|           | Perceived Health Rating - self                                                                  | health_rating            |
|           | DSM-5 Self-Rated Level 1 Cross-Cutting Symptoms Measure ??? Adult (modified)                      | mental_health_questions  |
|           | World Health Organization Disability Assessment Schedule 2.0 (WHODAS 2.0)                       | whodas                   |
| In-Person | Adverse Childhood Experiences (ACEs)                                                            | ace                      |
|           | Chemistry Panel                                                                                 | acute_care               |
|           | Beck Anxiety Inventory (BAI)                                                                    | bai                      |
|           | Beck Depression Inventory-II (BDI-II)                                                           | bdi                      |
|           | Creatine Kinase, C-reactive Protein, TSH                                                        | blood_chemistry          |
|           | Complete Blood Count with Differential                                                          | cbc_with_differential    |
|           | Medical and mental health diagnosis, medications, physical exam, lab findings, vital signs, BMI | clinical_variable_form   |
|           | Family Interview for Genetic Studies (FIGS)                                                     | figs                     |
|           | Hepatic Panel                                                                                   | hepatic                  |
|           | Kaufman Brief Intelligence Test 2nd Edition (KBIT-2) and Visual Analogue of Effort Scale (VAS)  | kbit2_vas                |
|           | MRI Variables form                                                                              | mri_variables            |
|           | NIH Toolbox measures                                                                            | nih_toolbox              |
|           | Viral markers (Hepatitis B, C and HIV)                                                          | other                    |
|           | Perceived Health Rating - clinician                                                             | perceived_health_rating  |
|           | Research participation satisfaction survey                                                      | satisfaction             |
|           | Structured Clinical Interview for DSM-5 Disorders (SCID-5)                                      | scid5                    |
|           | Urine drug screen and pregnancy test (if indicated)                                             | urine_chemistry          |

## Data Preparation Notes

In many of the Clinical Measures data files, there exist some `-999` values. `-999` means there was no response though a response was possible. The question may have been skipped over by the participant or the question flow. `-777` appears in the Edinburgh Handedness Inventory (EHI) as well. `-777` means there is no data available for a response. The question was not presented or asked to the participant.

The data were prepared using the following tools and filename mappings.

### Biological and Physiological Measures Data

The `01_cris_clean_up.py` python script contains the functions used to clean and convert the spreadsheet with clinical measures to BIDS-standard TSV files and their data dictionaries to BIDS-standard JSON files.

### Clinical Measures Data

The `02_ctdb_clean_up.py` python script contains the functions used to clean and convert the spreadsheet downloaded from CTDB to BIDS-standard TSV files as well as their respective data dictionaries converted to BIDS-standard JSON files.

Some of the python functions common to both scripts were defined in `rvoldefinitions.py`

### BIDS-standard MEG Files

Data collected by the NIMH MEG Core was converted to BIDS-standard files using the MNE BIDS package. Associated notebooks: `1_mne_bids_extractor.ipynb` & `2_bids_editor.ipynb`. In addition, event codes and correct timings were generated with `hv_process.py` script, and the fiducial locations from the AFNI HEAD files were generated using the `export_tags.py` script. 

### BIDS-standard MRI

We used the `heudiconv` tool to convert MRI DICOM files to BIDS-standard files with the associated script: `hv_protocol_heuristic.py`. A modified workflow of `pydeface` was used to deface structural scans with the associated python script: `hv_protocol_pydeface_workflow.py`

Each participant received either the ADNI3 or the ABCD protocol, not both, during their MRI/MEG visit. T1w scans with acquisition label `fspgr` are ADNI3 protocol sequence and scans with `mprage` acquisition labels are ABCD protocol sequence.

### OpenNeuro BIDS File/Folder Tree

Below is a BIDS-compliant file/folder tree as it appears for subjects on OpenNeuro.

```shell
sub-ON<subject>
    ????????? ses-01
        ????????? anat
        ???   ????????? sub-ON<subject>_ses-01_acq-<desc>_run-<index>_<suffix>.<json|nii.gz>
        ????????? asl
        ???   ????????? sub-ON<subject>_ses-01_run-<index>_asl.<json|nii.gz>
        ????????? dwi
        ???   ????????? sub-ON<subject>_ses-01_run-<index>_dwi.<bvec|bval|json|nii.gz>
        ????????? fmap
        ???   ????????? sub-ON<subject>_ses-01_acq-<desc>_dir-<direction>_run-<index>_epi.<bvec|bval|json|nii.gz>
        ????????? func
        ???   ????????? sub-ON<subject>_ses-01_task-<taskname>_run-<index>_<suffix>.<json|nii.gz>
        ????????? meg
        ???   ????????? sub-ON<subject>_ses-01_task-<taskname>_run-01_<meg|coordsystem>.json
        ???   ????????? sub-ON<subject>_ses-01_task-<taskname>_run-01_<channels|events>.tsv
        ???   ????????? sub-ON<subject>_ses-01_task-<taskname>_run-01_meg.ds
        ???       ????????? BadChannels
        ???       ????????? bad.segments
        ???       ????????? ClassFile.cls
        ???       ????????? MarkerFile.mrk
        ???       ????????? params.dsc
        ???       ????????? processing.cfg
        ???       ????????? sub-ON<subject>_ses-01_task-<taskname>_run-01_meg.<extension>
        ???       ????????? sub-ON<subject>_ses-01_task-<taskname>_run-01.xml
        ????????? sub-ON<subject>_ses-01_scans.<json|tsv>
```

Definitions:

- `<subject>` = subject number
- `<taskname>` = task name: `airpuff`, `artifact`, `gonogo`, `haririhammer`, `movie`, `oddball`, `sternberg`
- `<desc>` = placeholder for acquisition label for a given suffix
- `<direction>` = flipped, unflipped
- `<index>` = run number/index
- `<suffix>` = placeholder to indicate the scan type
  - `T1w`: `<desc>` = `fspgr`, `mprage`, `fse`, `highreshippo`
  - `T2w`: `<desc>` = `abcdcube`, `cube`, `frfse`
  - `FLAIR`: `<desc>` = `adni2d`, `2d`, `3d`, `t2`
  - `epi`: `<desc>` = `dwib1000`, `dwi`, `resting`
  - `T2star`
  - `bold`
  - `meg`
  - `asl`
- `<extension>`: indicates meg data files' type = `acq`, `bak`, `hc`, `hist`, `infods`, `meg4`, `newds`, `res4`, `xml`
