import os
import argparse

from random import sample
from enum import Enum

import cv2
import numpy as np

from log_handler import Logger, LogTemplates, runtime

logger = Logger(__name__)


class Constants(Enum):
    """Stores the constants for the module."""
    JPEG_DIR = "DAVIS/JPEGImages/480p"
    ANNT_DIR = "DAVIS/Annotations/480p"
    SET_COUNT = 90
    OPACITY = 0.5
    FPS = 24


def get_blended_frame(base_frame: str, set_name: str) -> np.ndarray:
    """Creates a blended frame from base and overlay layers from the dataset.

    Args:
        base_frame (str): name of the base layer file in the set
        set_name (str): name of the set of the images in the dataset

    Returns:
        np.ndarray: numpy array, which stores blended image frame.
    """

    # Changing the filename extension to get the overlay filename.
    overlay_frame = os.path.splitext(base_frame)[0] + '.png'

    # Loading base and overlay image objects.
    base_layer = cv2.imread(os.path.join(Constants.JPEG_DIR.value,
                                         set_name, base_frame))
    overlay_layer = cv2.imread(os.path.join(Constants.ANNT_DIR.value,
                                            set_name, overlay_frame))

    # Blending two image objects and append it into the list.
    return cv2.addWeighted(base_layer, 1 - Constants.OPACITY.value,
                           overlay_layer, Constants.OPACITY.value, 0)


def get_frame_size(image_set: str) -> tuple[int]:
    """Reads the metadata from the first image in the specified set of the
    images of the dataset. Returns dimensions of the image.

    Args:
        image_set (str): name of the set of the images in the dataset

    Returns:
        tuple[int]: dimensions of the image (width, height)
    """
    first_frame = os.listdir(os.path.join(Constants.JPEG_DIR.value,
                                          image_set))[0]
    frame_width, frame_height = cv2.imread(
        os.path.join(Constants.JPEG_DIR.value, image_set, first_frame),
        cv2.IMREAD_ANYDEPTH).shape[1::-1]

    return frame_width, frame_height


@runtime
def create_video(sets_number: int, output_path: str) -> None:
    """Creates a video from specified sets amount of images from DAVIS
    dataset."""
    logger.info(LogTemplates.STARTED.format(sets_number))
    try:
        # Reading the list of the sets in the dataset and choosing specified
        # amount of random set names.
        image_sets = sample(os.listdir(Constants.JPEG_DIR.value), sets_number)
    except FileNotFoundError:
        logger.error(LogTemplates.NO_DATASET)
        return

    # Obtaining the dimensions of the result video.
    video_width, video_height = get_frame_size(image_sets[0])
    # Creating video objects for adding frames into.
    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'),
                            Constants.FPS.value, (video_width, video_height))

    for set_name in image_sets:
        # Iterating over each set of the image sets, reading list of the
        # files in the set.
        base_frames = os.listdir(os.path.join(Constants.JPEG_DIR.value,
                                              set_name))
        for base_frame in base_frames:
            # Creating blended frames for each frame, writing them into video.
            video.write(get_blended_frame(base_frame, set_name))

    # Saving resulting video and write to the log.
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
