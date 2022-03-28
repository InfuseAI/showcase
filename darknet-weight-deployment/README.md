# Darknet model deployment

In this example, we demonstrate how to build a custom pre-packaged server for [AlexeyAB/darknet YOLO v4](https://github.com/AlexeyAB/darknet).

The server detect objects in an image

- **Input:** (binData) the bytes of image
- **Output:** Probability, object name and the location.
   - Example:
   ```json
   {"jsonData":{"output":[["person","27.28",495,832,180,577],["person","95.97",250,493,48,633],["person","98.96",519,809,90,424]]},"meta":{"requestPath":{"model":"infuseaidev/darknet-prepackaged:v0.1.0"}}}
   ```
- **Model Files:** The tree structure is shown below.
  ```bash
  <model uri>
   ├── coco.data
   ├── coco.names
   ├── model.json
   ├── yolov4.weight
   └── yolov4.cfg
  ```

## How to build the docker image

```bash
$ make build
$ make push
```

## How to run the docker image

1. Download files:
   - yolov4.weight
      ```bash
      wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
      ```
   - yolov4.cfg
      ```bash
      wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
      ```
   - coco.names
      ```bash
      wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.names
      ```
1. Write the content:(or you can use `example` folder files.)
   - coco.data
      ```bash
      classes=80
      names=/mnt/models/coco.names
      ```
   - model.json
      ```json
      {
         "model_cfg": "yolov4.cfg",
         "label_data": "coco.data",
         "model_weight": "yolov4.weights",
         "batch_size": 1,
         "model_threshold": 0.6
      }
      ```
1. Put all files into `models/` folder
1. Run the image
   ```docker
   docker run --name darknet --rm -it -p 5000:5000 -v $PWD/models:/mnt/models <darknet-yolov4-image-name>
   ```

## How to submit a post request

1. Prepare a picture
1. Use the following python code to draw the result in picture.
   ```python
   import time
   import base64
   import json
   import cv2
   import numpy as np

   # Please change variables: 
   # image path, primehub_deployment_url and probability_threshold

   image_path = 'infuseai.jpeg'
   primehub_deployment_url = <primehub-deployment-url>
   probability_threshold = 50

   # Input
   files = {
      'binData': (image_path, open(image_path, 'rb')),
   }

   # Prediction
   response = requests.post(primehub_deployment_url, files=files)

   # Output to Json
   string = json.loads(response.content.decode("utf-8"))

   # Draw the result
   img = cv2.imread(image_path)
   for rectangle in string['jsonData']['output']:
      if float(rectangle[1]) >= probability_threshold:
         pt1 = (rectangle[2], rectangle[4])
         pt2 = (rectangle[3], rectangle[5])
         cv2.rectangle(img, pt1, pt2, (0, 0, 255), 1)
         cv2.putText(img,
                     f"{rectangle[0]}[{rectangle[1]}]",
                     (pt1[0], pt1[1] - 5),
                     cv2.FONT_HERSHEY_SIMPLEX,
                     0.5,
                     (0, 0, 255),
                     2
         )
         cv2.imwrite('./{}.jpg'.format(int(time.time())), img)
   ```
3. You can see the result in `<time>.jpeg`.