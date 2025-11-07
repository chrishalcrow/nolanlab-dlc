from argparse import ArgumentParser
from pathlib import Path
import deeplabcut as dlc
import shutil
import os

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
    if data_folder is None:
        data_folder = "/exports/eddie/scratch/chalcrow/wolf/data"
    data_folder = Path(data_folder)

    deriv_folder = parser.parse_args().deriv_folder
    if deriv_folder is None:
        deriv_folder = "/exports/eddie/scratch/chalcrow/wolf/derivatives"
    deriv_folder = Path(deriv_folder)

    config_path = "/exports/eddie/scratch/chalcrow/wolf/code/models/of_cohort12-krs-2024-10-30/config.yaml"

    mouse_day_session_folder = list(data_folder.glob(f'M{mouse}_D{day}_*{session}'))[0]

    video_path = str(mouse_day_session_folder / f"sub-{mouse}_day-{day}_ses-{session}_video.avi")
    video_filename = video_path.split("/")[-1]
    save_path = str(deriv_folder / f"M{mouse}/D{day}/{session}/dlc_output/")

    derivatives_video_path = save_path + video_filename
    _ = shutil.copy(video_path, derivatives_video_path)

    dlc.analyze_videos(config_path, [derivatives_video_path], save_as_csv=True, destfolder=save_path)
    dlc.filterpredictions(config_path, [derivatives_video_path])
    dlc.create_labeled_video(config_path, [derivatives_video_path], save_frames=False)
    dlc.plot_trajectories(config_path, [derivatives_video_path])

    os.remove(derivatives_video_path)

if __name__ == "__main__":
    main()