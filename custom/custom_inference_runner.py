import os
import cv2
import time
import json
import base64
import requests
import numpy as np
from datetime import datetime

from requests.models import Response
from .infer import Inference
from .config import TEST_OPTION, INFERENCE_OPTION
from .infer_config import infer_config
from pathlib import Path

start_date = datetime.now().strftime("%y%m%d_%H%M%S.%f").split('_')[0]
inference = Inference(infer_config)

def run(meta, data, push):
    global start_date
    # preprocessed = np.array(data[0])
    # preprocessed = np.ascontiguousarray(data[0])
    # preprocessed = cv2.cvtColor(preprocessed, cv2.COLOR_BGR2RGB)
    # preprocessed = preprocessed[:,:,:,(2,1,0)]
    if INFERENCE_OPTION['inference-process']:
        date = curr_date_check(start_date)
        save_path_check(date)
        result = []
        for image in data[0]:
            image_as_bytes = base64.b64encode(image)
            response = requests.post('http://localhost:8080/predictions/resnet101', data=image_as_bytes)
            boool = response.content.decode()
            if boool == 'true':
                result.append(True)
            else:
                result.append(False)

        # result, annotations = inference.check_tp(preprocessed, date)
        # if len(annotations)==0:
        #     pass
        # for annot in annotations:
        #     file_name = annot['file_name'].split('.p')[0]
        #     with open(f"/app/json_result/{date}/{file_name}.json", 'w') as fp:
        #         json.dump(annot,fp)

    else:
        result = [None, None, None, None, None, None]
    if TEST_OPTION['mode'] == 'delay':
        _id = meta[0][0]['id']
        if _id % 2 == 0:
            print('Delay inference test')
            time.sleep(TEST_OPTION['delay_time'])
    dataset = []
    dataset.append(result)
    dataset.append(data[0])
    push(meta[0], dataset)


def save_path_check(date):
    Path(f'/app/json_result/{date}').mkdir(exist_ok=True, parents=True)
    Path(f'/app/dot_result/{date}').mkdir(exist_ok=True, parents=True)
    Path(f'/app/shortcut_result/{date}').mkdir(exist_ok=True, parents=True)
    Path(f'/app/inference_result/{date}').mkdir(exist_ok=True, parents=True)


def curr_date_check(date):
    curr_date = datetime.now().strftime("%y%m%d_%H%M%S.%f").split('_')[0]
    if date != curr_date:
        date = curr_date
    return date

