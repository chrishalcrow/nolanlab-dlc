from eddie_helper.make_scripts import run_python_script

from argparse import ArgumentParser
from pathlib import Path

def main():

    parser = ArgumentParser()

    parser.add_argument('mouse')
    parser.add_argument('day')
    parser.add_argument('session')
    parser.add_argument('--data_folder', default=None)
    parser.add_argument('--deriv_folder', default=None)

    mouse = int(parser.parse_args().mouse)
    day = int(parser.parse_args().day)
    session = parser.parse_args().session
    data_folder = parser.parse_args().data_folder
    deriv_folder = parser.parse_args().deriv_folder


    run_python_name = f"M{mouse}D{day}{session}dlc"
#    stageout_job_name = f"M{mouse}D{day}{sessions[0]}out" 

    python_arg = f"$HOME/.local/bin/uv run /exports/eddie/scratch/chalcrow/wolf/code/nolanlab-dlc/dlc_on_eddie.py {mouse} {day} {session} {data_folder} {deriv_folder}"

    run_python_script(python_arg, cores=8, email="chalcrow@ed.ac.uk", staging=False, job_name=run_python_name)
