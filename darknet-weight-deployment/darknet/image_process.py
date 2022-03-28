import darknet
import numpy as np
import cv2


def image_detection(image, network, class_names, class_colors, thresh):
    # Darknet doesn't accept numpy images.
    # Create one with image we reuse for each detect
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    aspectRatio = [image.shape[0]/width, image.shape[1]/height]

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(
        image_rgb, (width, height), interpolation=cv2.INTER_LINEAR)
    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(
        network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    detections_list = cvDrawBoxes(detections, image, class_colors, aspectRatio)
    return detections_list


def cvDrawBoxes(detections, img, class_colors, aspectRatio):
    detections_list = []
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]

        xmin = int(aspectRatio[1]*round(x - (w / 2)))
        xmax = int(aspectRatio[1]*round(x + (w / 2)))
        ymin = int(aspectRatio[0]*round(y - (h / 2)))
        ymax = int(aspectRatio[0]*round(y + (h / 2)))

        detections_list.append(
            [detection[0], detection[1], xmin, xmax, ymin, ymax])
    return detections_list
