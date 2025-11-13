from eddie_helper.make_scripts import run_python_script

from argparse import ArgumentParser
from pathlib import Path

def main():

    parser = ArgumentParser()

    parser.add_argument('mouse')
    parser.add_argument('day')
    parser.add_argument('session')
    parser.add_argument('bodypart')
    parser.add_argument('--data_folder', default="")
    parser.add_argument('--deriv_folder', default="")

    mouse = int(parser.parse_args().mouse)
    day = int(parser.parse_args().day)
    session = parser.parse_args().session
    bodypart = parser.parse_args().bodypart

    data_folder = parser.parse_args().data_folder
    deriv_folder = parser.parse_args().deriv_folder


    run_python_name = f"M{mouse}D{day}{session}dlc"
#    stageout_job_name = f"M{mouse}D{day}{sessions[0]}out" 

    uv_directory = "/exports/eddie/scratch/chalcrow/wolf/code/nolanlab-dlc/"
    python_arg = f"dlc_on_comp.py {mouse} {day} {session} {bodypart} {data_folder} {deriv_folder}"

    run_python_script(uv_directory, python_arg, cores=8, email="chalcrow@ed.ac.uk", staging=False, job_name=run_python_name)

if __name__ == "__main__":
    main()