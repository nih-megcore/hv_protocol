import argparse
import json
import subprocess
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Add fiducial locations to T1w JSON sidecars of subjects with MEG data associated with them.")

    parser.add_argument('-b', '--bids-dir', type=Path, action='store', dest='bids_dir', help="Path to input directory.")
    parser.add_argument('-j', '--jsons-with-fiducials', type=Path, action='store', dest='correct_jsons',
                        help="Path to directory with JSON sidecars containing AnatomicalLandmarkCoordinates field.")
    args = parser.parse_args()

    return args.bids_dir.resolve(), args.correct_jsons.resolve()


def run_shell_cmd(cmdstr):
    pipe = subprocess.Popen(cmdstr, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, encoding='utf8', shell=True)
    return pipe.stdout


def add_key_to_sidecar(src_json, dest_json, field):
    src_fobj = open(src_json, 'r')
    src_data = json.load(src_fobj)
    if field in src_data.keys():
        dest_fobj = open(dest_json, 'r')
        try:
            dest_data = json.load(dest_fobj)
            dest_data['AnatomicalLandmarkCoordinates'] = src_data['AnatomicalLandmarkCoordinates']
            with open(dest_json, 'w') as f:
                json.dump(dest_data, f, indent=4, ensure_ascii=True)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print(f'Decoding JSON sidecar at {src_json} has failed')


    else:
        print(
            f'No key-value pair with {field} as key in {src_json}. Please provide a json sidecar path with the field.')

    return None


def main():
    bids_dir, input_jsons = parse_arguments()
    for sidecar in list(input_jsons.glob('*')):
        entities = sidecar.name.split('_')
        dest_jsons = list(bids_dir.joinpath(entities[0], entities[1], 'anat').glob('*T1w.json'))
        for dest_json in dest_jsons:
            add_key_to_sidecar(sidecar, dest_json, 'AnatomicalLandmarkCoordinates')


if __name__ == "__main__":
    main()
