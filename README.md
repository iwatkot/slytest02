<a href="https://codeclimate.com/github/iwatkot/slytest02/maintainability"><img src="https://api.codeclimate.com/v1/badges/f026010dd2a8a686d17c/maintainability" /></a>

## Overview
The repo contains the script, which creates a video from sequences from [DAVIS dataset](https://davischallenge.org/davis2017/code.html).<br>
**Note:** the script requires DAVIS dataset to be present in the directory where the script will be launched.<br>
The script uses base images from `JPEGImages` directory and annotation images from `Annotations` to create an example video with annotation visualization. The script is using `cv2` and `numpy`. In addition the repo contains a simple logger, which uses Python's built-in logging module, and writes logs both to the file and stdout. The log_handler module is also contains a decorator for measuring the runtime of the functions.<br>

## Get started
_The script is designed to be launched from the command line with different arguments._<br><br>
**Example of splitting the image:** `python3 create_video.py --output_path path/to/file.mp4 --sets_number <>`<br>
Where both arguments are required: output path to the result file, and number of sets which will be used to create the video.<br>
<br>

## Asciinema examples
**Creating a video:**<br>
[![asciicast](https://asciinema.org/a/OgZ5rtlkrvns3r5g2rOK8dHgt.svg)](https://asciinema.org/a/OgZ5rtlkrvns3r5g2rOK8dHgt)<br>
<br>

## Report
I started the approach to the solution with understanding how images in `Annotations` directory are storing the useful data. It takes some tome and several tries, since I started to solving the problem with incorrect tools (I tried to handle images as masks with cv2.bitwise_and and the result was far from expected), which leads me to errors, trying and researching. After this problem was solved just with simple image blending, the rest part of the task didn't provide complex challenges. The easiest way was to handle each frame of the result video, pack it into the list and then create a video frame by frame. Since I already completed first test task, I was able to re-use my code and copy-pasted the logger and argparser (with adoptation of course).