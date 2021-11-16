import os
import logging
import time
import cv2

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


class CollectImagesStream:
    def __init__(self, config):
        self.cap = cv2.VideoCapture(config.video_source)
        self.frame_rate = config.rest_time
        self.folder_path = config.folder_path
        self.max_num_images = config.max_num_images
        self.__create_folder()

    def __create_folder(self):
        # Create target Directory if don't exist
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            logging.info("Directory {} created.".format(self.folder_path))
        else:
            logging.warning("Directory {} already exists.".format(self.folder_path))

    def video_capture_process(self):
        # Initial number of images
        num_image = 1

        while self.cap.isOpened():
            # Init parameter
            frame_id = int(self.cap.get(1))

            # Read image
            ret, frame = self.cap.read()

            if ret:
                # Save location
                image_path = os.path.join(
                    self.folder_path, "image_{}_num_{}.jpg".format(frame_id, num_image)
                )

                # Save image
                cv2.imwrite(image_path, frame)

                # Calculate number of images
                num_image += 1

                # Rest for a while.
                time.sleep(self.frame_rate)

                # If exceed max number of images, then break the process
                if num_image >= self.max_num_images:
                    logging.info("Finish saving {} images.".format(self.max_num_images))
                    break
            else:
                break

        # Release video capture.
        self.cap.release()
