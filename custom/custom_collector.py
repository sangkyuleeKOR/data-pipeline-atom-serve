import os
from datetime import datetime
from .camera.camera import create_devices_with_tries, create_device_and_settings, destroy_devices
from . import plc_api
from .config import COLLECT_OPTION
from .config import TEST_OPTION
import time
import numpy as np
import cv2
from collections import deque

def run(push, queue):
    print('collector run')
    try:
        print('start connect camera')
        device = create_device_and_settings()
        print('success connect camera')
        plc_api.send_message(1, "M750") 

        print('=================')
        print('Start collect')
        print('Mode : save origin image:', COLLECT_OPTION['collect_save_img'], '/ count:', COLLECT_OPTION['collect_count'])
        print('Mode : save crop image:', COLLECT_OPTION['collect_save_crop_img'])
        print('Path : save image path:', COLLECT_OPTION['collect_save_img_path'])
        print('Cycle :', COLLECT_OPTION['collect_cycle'], 's')
        print('Test mode :', TEST_OPTION['mode'])
        print('=================')

        plc_status = 1
        save_count = 0
        plc_queue = deque(maxlen=4)
        while device.start_stream(1):
            print('start camera stream')
            while True:
                print('running')
                while True:
                    time.sleep(0.01)
                    current_plc_status = plc_api.get_value()
                    #print('plc_status : ', plc_status, ' current_plc_status : ', current_plc_status, ' time : ' , datetime.now())
                    if not plc_status == current_plc_status and len(plc_queue) == 4 and len(set(plc_queue)) == 1:
                        plc_status = current_plc_status
                        if plc_status == 1 and 0 in set(plc_queue):
                            #print('plc_queue : ', plc_queue, ' result : ', len(set((plc_queue))),  ' time : ' , datetime.now())
                            plc_queue.append(current_plc_status)
                            break
                        plc_queue.append(current_plc_status)
                    else:
                        plc_queue.append(current_plc_status)
                t1 = datetime.now()
                #####sleep#####
                # time.sleep(0.15)
                image_buffer = device.get_buffer()
                # (width, height, 3) -> (width, height, 1)
                img = np.ctypeslib.as_array(image_buffer.pdata,(image_buffer.height,image_buffer.width, 3))
                #push({'type': 6-i, 'time': t1}, img)
                device.requeue_buffer(image_buffer)
                time.sleep(0.05)
                queue.put(({'type': 6, 'time': t1}, img))
                if COLLECT_OPTION['collect_save_img'] and ((COLLECT_OPTION['collect_count'] < 0) or (save_count < COLLECT_OPTION['collect_count'])):
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(COLLECT_OPTION['collect_save_img_path']+f'{t1.strftime("%Y%m%d_%H%M%S.%f")}.png', img)
                    save_count += 1

    finally:
        destroy_devices()

def test_run(push, queue):
    print('=================')
    print('Start test runner')
    print('Mode : save origin image:', COLLECT_OPTION['collect_save_img'], '/ count:', COLLECT_OPTION['collect_count'])
    print('Mode : save crop image:', COLLECT_OPTION['collect_save_crop_img'])
    print('Path : save image path:', COLLECT_OPTION['collect_save_img_path'])
    print('Cycle :', COLLECT_OPTION['collect_cycle'], 's')
    print('Test mode :', TEST_OPTION['mode'])
    print('=================')
    try:
        while True:
            files = [f for f in os.listdir('img_save') if os.path.isfile(os.path.join('img_save', f))]
            files = sorted(files)
            for f_path in files:    
                with open('img_save/' + f_path, 'rb') as f:
                    data = f.read()
                    queue.put(({'type': 6, 'time': datetime.now()}, data))
                    time.sleep(COLLECT_OPTION['collect_cycle'])
            break
    finally:
        print('destroy')

if __name__=='__main__':
    test_run(None, None)

