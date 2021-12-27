from . import publisher_cloud
from .publisher_cloud import Publisher_cloud
import numpy as np
from .config import CLOUD_OPTION
import shutil
from pathlib import Path
import cv2
import os

# mqtt_client = Publisher_cloud()
# mqtt_client.start()

results = {}
collect_times = {}
save_dir_name = {}

count = 0

def run(meta, data, push):
    global count
    drop_position = None
    print('Model output : ', data[0][0])
    for _meta, _data, _image in zip(meta[0], data[0][0], data[0][1]):
        _id = _meta['id']
        collect_time = _meta['time']
        if 'dropped' in _meta:
            drop_position = _id
        is_normal = _data
        if _id in results:
            results[_id].append(is_normal)
            save_image(save_dir_name[_id], _image, len(results[_id]))
        else: 
            results[_id] = [is_normal]
            save_dir_name[_id] = "{:%Y%m%d%H%M%S%f}".format(collect_time)
            save_image(save_dir_name[_id], _image, 1)
    print('Result set : ', results)

    if drop_position != None:
        checked = results[drop_position]
        del results[drop_position]
        if len(checked) < 6:
            print('Skip position:', drop_position, '/ length is under 6', '\n')
            return
        push_meta = {'id': drop_position, 'time': collect_time}
        #if checked == 'found empty':
        #    result = True
        result = (all(checked))
        push_data = result
        #drop_position = None
 
        push(push_meta, push_data)
    #     if not result:
    #         send_image(drop_position, result)
    #     elif count > CLOUD_OPTION['true_product_period'] and result:
    #         send_image(drop_position, result)
    #         count = 0
    #     shutil.rmtree('/data/' + str(save_dir_name[drop_position]))
    #     del save_dir_name[drop_position]
    #     drop_position = None
    # count += 1

def save_image(collect_time, image, count):
    if not os.path.isdir('/data'):
        os.mkdir('/data')
    if not os.path.isdir('/data/' + str(collect_time)):
        os.mkdir('/data/' + str(collect_time))
    save_path = '/data/' + str(collect_time) + '/' + str(count) + '.jpg'    
    cv2.imwrite(save_path, image)
    

# def send_image(drop_position, result):
#     collect_time = save_dir_name[drop_position]
#     result_meta = '||' + str(result)
#     dir_path = Path('/data/' + str(collect_time))
#     files = sorted(dir_path.iterdir(), reverse=True)
#     file_count = '||' + str(len(files))
#     for index, file in enumerate(files):
#         with open(file, 'rb') as f:
#             data = f.read()
#         mqtt_client.publish('tampon/', data + b'\x00' + collect_time.encode() + result_meta.encode() + file_count.encode() + b'\x00')
#     print('id : ', drop_position,' send image is success')
#    nparray = np.array(data)
#    byte = nparray[0].tobytes()
#    mqtt_client.publish('tampon/', byte + b'\x00')
#    nparray = np.delete(nparray, 0, axis=0)
#    for img in nparray:
#        byte = img.tobytes()
#        mqtt_client.publish('tampon/', byte + b'\x01')
#    url = CLOUD_OPTION['address'] 
#    headers = {'Content-Type': 'application/json; charset=utf-8', 'Inference-Result': result, 'Collect-Time' : collect_time}
#    data = {'data' : nparray}
#    response = requests.post(url, headers=headers, json=data)
    
