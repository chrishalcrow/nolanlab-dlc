from argparse import ArgumentParser
from pathlib import Path
import deeplabcut as dlc
import shutil
import os
import pandas as pd
import cv2

def make_cropped_video(video_path, output_path, cropping):
    
    if cropping is None:
        _ = shutil.copy(video_path, output_path)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Initialize frame counter
    cnt = 0
    
    x,y,w,h = cropping

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    # Now we start
    while(cap.isOpened()):
        ret, frame = cap.read()

        cnt += 1 

        if ret==True:
            crop_frame = frame[y:y+h, x:x+w]

            out.write(crop_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():

    parser = ArgumentParser()

    parser.add_argument('mouse')
    parser.add_argument('day')
    parser.add_argument('session')
    parser.add_argument('bodypart')
    parser.add_argument('--data_folder', default=None)
    parser.add_argument('--deriv_folder', default=None)

    mouse = int(parser.parse_args().mouse)
    day = int(parser.parse_args().day)
    session = parser.parse_args().session
    bodypart = parser.parse_args().bodypart

    if bodypart not in ['tongue', 'eye', 'body']:
        raise UserWarning('bodypart must be lick eye or body!')

    data_folder = parser.parse_args().data_folder
    if data_folder is None:
        data_folder = "/exports/eddie/scratch/chalcrow/wolf/data"
    data_folder = Path(data_folder)

    deriv_folder = parser.parse_args().deriv_folder
    if deriv_folder is None:
        deriv_folder = "/exports/eddie/scratch/chalcrow/wolf/derivatives"
    deriv_folder = Path(deriv_folder)

    if bodypart == "tongue":
        config_path = "/exports/eddie/scratch/chalcrow/wolf/code/models/c12_lick-chris-2024-10-03/config.yaml"
    elif bodypart == "eye":
        config_path = "/exports/eddie/scratch/chalcrow/wolf/code/models/vr-hc-2024-03-14_eddie/config.yaml"
    elif bodypart == "body":
        config_path = "/exports/eddie/scratch/chalcrow/wolf/code/models/of_cohort12-krs-2024-10-30/config.yaml"

    mouse_day_session_folder = list(data_folder.glob(f'M{mouse:02d}_D{day:02d}_*{session}'))[0]

    video_path = str(mouse_day_session_folder / f"M{mouse:02d}_D{day:02d}_{session}_side_capture.avi")

    save_path = deriv_folder / f"M{mouse:02d}/D{day:02d}/{session}/dlc_output_{bodypart}/"
    save_path.mkdir(parents=True, exist_ok=True)
    save_path = str(save_path)
    cropped_video_path = str(save_path / f"M{mouse:02d}_D{day:02d}_{session}_side_capture_{bodypart}.avi")

    #derivatives_video_path = save_path + "/" + video_filename
    #_ = shutil.copy(video_path, derivatives_video_path)

    if bodypart in ["eye", "tongue"]:
        all_crop_info = pd.read_csv(f"wolf_crops/{bodypart}_crops_wolf.csv")
        x,y,w,h = all_crop_info.query(f'mouse == {mouse} & day == {day}')[['x','y','w','h']].values[0]
        cropping  =  [x, y, w, h]
    else:
        cropping = None

    make_cropped_video(video_path, cropped_video_path, cropping)

    dlc.analyze_videos(
        config_path, 
        [cropped_video_path], 
        save_as_csv=True, 
        destfolder=save_path,
    )
    dlc.filterpredictions(config_path, [cropped_video_path])
    dlc.create_labeled_video(config_path, [cropped_video_path], save_frames=False)
    dlc.plot_trajectories(config_path, [cropped_video_path])

    os.remove(cropped_video_path)

if __name__ == "__main__":
    main()