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

    config_path = "/exports/eddie/scratch/chalcrow/wolf/code/models/c12_lick-chris-2024-10-03/config.yaml"

    mouse_day_session_folder = list(data_folder.glob(f'M{mouse:02d}_D{day:02d}_*{session}'))[0]

    video_path = str(mouse_day_session_folder / f"M{mouse:02d}_D{day:02d}_{session}_side_capture.avi")
    video_filename = video_path.split("/")[-1]
    save_path = deriv_folder / f"M{mouse:02d}/D{day:02d}/{session}/dlc_output/"
    save_path.mkdir(parents=True, exist_ok=True)
    save_path = str(save_path)

    derivatives_video_path = save_path + "/" + video_filename
    _ = shutil.copy(video_path, derivatives_video_path)

    x = 300
    y = 580
    w = 350
    h = 350

    dlc.analyze_videos(
        config_path, 
        [derivatives_video_path], 
        save_as_csv=True, 
        destfolder=save_path,
        cropping = [x, x+w, y, y+h], 
    )
    dlc.filterpredictions(config_path, [derivatives_video_path])
    dlc.create_labeled_video(config_path, [derivatives_video_path], save_frames=False)
    dlc.plot_trajectories(config_path, [derivatives_video_path])

    os.remove(derivatives_video_path)

if __name__ == "__main__":
    main()