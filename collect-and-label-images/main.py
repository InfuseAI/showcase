import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
import time
import argparse
from src.collect_images_video import CollectImagesVideo
from src.collect_images_stream import CollectImagesStream

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_source", help="The source type of video.(stream/video)", type=str, default = "video")
    parser.add_argument("--video_path", help="The path of video.", type=str, default = "./data/video/demo_video.mp4")
    parser.add_argument("--rest_time", help="The time needed to rest.", type=int, default = 1)
    parser.add_argument("--folder_path", help="Folder path", type=str, default = "./data/{}/images/".format(int(time.time())))
    parser.add_argument("--max_num_images", help="The maximum number of images", type=int, default = 10)
    args = parser.parse_args()
    if args.video_source == "video":
        collect_images = CollectImagesVideo(args)
        collect_images.video_capture_process()
    elif args.video_source == "stream":
        collect_images = CollectImagesStream(args)
        collect_images.video_capture_process()
    else:
        logging.error("video source type error.")