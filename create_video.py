import os
import pathlib
import argparse

from random import sample
from enum import Enum

import cv2
import numpy

from log_handler import Logger, LogTemplates, runtime

logger = Logger(__name__)


class Constants(Enum):
    """Stores the constants for the module."""
    JPEG_DIR = "DAVIS/JPEGImages/480p"
    ANNT_DIR = "DAVIS/Annotations/480p"
    SET_COUNT = 90
    OPACITY = 0.5
    FPS = 24


def get_frames_set(set_name: str) -> list[numpy.ndarray]:
    """Creates a sequence of frames with base imaged overlayed by an
    annotation."""
    frames_set = []

    # Getting list of base frame files in the set directory.
    base_frames = os.listdir(os.path.join(Constants.JPEG_DIR.value, set_name))
    for base_frame in base_frames:
        # Changing the filename extension to get the overlay filename.
        overlay_frame = f"{pathlib.Path(base_frame).stem}.png"

        base_layer = cv2.imread(os.path.join(Constants.JPEG_DIR.value,
                                             set_name, base_frame))
        overlay_layer = cv2.imread(os.path.join(Constants.ANNT_DIR.value,
                                                set_name, overlay_frame))

        # Blending two image objects and append it into the list.
        frames_set.append(
            cv2.addWeighted(base_layer, 1 - Constants.OPACITY.value,
                            overlay_layer, Constants.OPACITY.value, 0))

    return frames_set


@runtime
def create_video(sets_number: int, output_path: str) -> None:
    """Creates a video from specified sets amount of images from DAVIS
    dataset."""
    logger.info(LogTemplates.STARTED.format(sets_number))
    try:
        image_sets = sample(os.listdir(Constants.JPEG_DIR.value), sets_number)
    except FileNotFoundError:
        logger.error(LogTemplates.NO_DATASET)
        return

    frames = []
    for image_set in image_sets:
        frames.extend(get_frames_set(image_set))
    logger.info(LogTemplates.FRAMES_CREATED.format(len(frames)))

    # Getting frame size from the first frame in the list.
    video_height, video_width, _ = frames[0].shape
    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'),
                            Constants.FPS.value, (video_width, video_height))

    # Writing all frames into the video object.
    for frame in frames:
        video.write(frame)
    video.release()
    logger.info(LogTemplates.VIDEO_CREATED)


def parse_arguments() -> argparse.Namespace:
    """Creates parser and reads arguments from the command line."""
    parser = argparse.ArgumentParser(description="Creates a video from"
                                     "DAVIS dataset sequences.")
    # Reading arguments from the command line.
    parser.add_argument("--sets_number", type=int,
                        help="number of sets to use (between 1 and 90)")
    parser.add_argument("--output_path", type=str,
                        help="path for the output file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    if args.sets_number not in range(1, Constants.SET_COUNT.value + 1):
        logger.error(LogTemplates.BAD_SET_NUMBER)
    else:
        create_video(args.sets_number, args.output_path)
