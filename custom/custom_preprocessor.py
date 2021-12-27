import numpy as np
import time
import os
import cv2
from datetime import datetime
from threading import Thread
from . import plc_api
from .config import COLLECT_OPTION
import matplotlib.pyplot as plt

class KeyStore:

    def __init__(self):
        self.ids = [1,2,3,4,5,6]
        self.start_point = 0
    
    def iter(self):
        for i in range(len(self.ids)):
            yield self.ids[(self.start_point + i) % len(self.ids)]

    def move_start_point(self):
        self.start_point = self.start_point + 1 if self.start_point != len(self.ids) - 1 else 0

class Timer:

    def start(self, request_id, offset, timeout): 
        current = datetime.now()
        delta = current - offset
        time.sleep(timeout - delta.total_seconds())
        #print('send timer ', 'request_id : ', request_id, 'value : ', 1)
        # plc_api.send_result(request_id, 0, 'timer')

key_store = KeyStore()
timer = Timer()
is_timer_start_count = 5

def rgb_extractor(image):
    result = []
    for i in range(0, 540, 80):
        area = image[i:i+80, 240:250]
        maximum = [abs(sum(value[:,2]) - sum(value[:,0])) for value in area]
        result.append(maximum.index(max(maximum)))
    
    return result


def image_crop(image):
    img_array = np.empty((6,80,320,3), dtype=np.uint8)
    image = cv2.resize(image, dsize=(720, 540))
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imsave('test.jpg',image)
    gap = rgb_extractor(image)
    img1 = image[gap[0]:gap[0]+80, COLLECT_OPTION['width'][0]:COLLECT_OPTION['width'][1]]
    img2 = image[80+gap[1]:gap[1]+160, COLLECT_OPTION['width'][0]:COLLECT_OPTION['width'][1]]
    img3 = image[160+gap[2]:gap[2]+240, COLLECT_OPTION['width'][0]:COLLECT_OPTION['width'][1]]
    img4 = image[240+gap[3]:gap[3]+320, COLLECT_OPTION['width'][0]:COLLECT_OPTION['width'][1]]
    img5 = image[320+gap[4]:gap[4]+400, COLLECT_OPTION['width'][0]:COLLECT_OPTION['width'][1]]

    if 480+gap[5] > 540:
        img6 = image[460:540, COLLECT_OPTION['width'][0]:COLLECT_OPTION['width'][1]]
    else:
        img6 = image[400+gap[5]:gap[5]+480, COLLECT_OPTION['width'][0]:COLLECT_OPTION['width'][1]]
    i=0
    for img in [img1, img2, img3, img4, img5, img6]:
        img_array[i,:] = img
        i+=1
    return img_array


# save_count = 0

def run(meta, data, push, debug=False):
    global is_timer_start_count
    collect_time = meta['time']
    if is_timer_start_count == 0:
        p = Thread(target=timer.start, args=(collect_time.timestamp(), collect_time, COLLECT_OPTION['collect_cycle']))
        p.start()
    else:
        is_timer_start_count -= 1
        
    if debug:
        img = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(img, -1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        
    croped = image_crop(img)

    if COLLECT_OPTION['collect_save_crop_img'] and ((COLLECT_OPTION['collect_count'] < 0)):
    
        t1 = datetime.now()
        for i, _croped in enumerate(croped):
            cv2.imwrite(COLLECT_OPTION['collect_save_crop_img_path']+f'{t1.strftime("%Y%m%d_%H%M%S.%f")}_{i}.png', _croped)

    meta_result = []
    gen = key_store.iter()
    for i, _croped in enumerate(croped):
        _meta = {'id': next(gen), 'time': collect_time}
        if i == 0:
            _meta['dropped'] = True
        meta_result.append(_meta)
    key_store.move_start_point()
    push(meta_result, croped)

