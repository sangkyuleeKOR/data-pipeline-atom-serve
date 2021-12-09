from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

img_dir = '/home/bomyung/data-pipeline-atom/inference_result'

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/getFile', methods=['POST'])
def getFile():
    params = request.values    
    date = params['date']

    recent_count = int(params['recentCount'])
    
    img_file_dir = (f'{img_dir}/{date.replace("-","")}')
    print(img_file_dir) 

    if os.path.isdir(img_file_dir):
        file_list = os.listdir(img_file_dir)
        file_list_img = [file for file in file_list if file.endswith('.jpg')]

        file_count = len(file_list_img)
        
        if(file_count > recent_count): 
            file_list_img.sort()
            
            # 너무많은 이미지파일 요청이 오면 안되기 때문에
            # 파일갯수가 최근 파일갯수보다 30개이상 많으면 최대 30개까지만 전송
            # 최초로 켯을때는 마지막 10개 파일만 전송
            if(30 >= file_count-recent_count and file_count != 0): 
                file_list_img = file_list_img[recent_count:]
            else: 
                file_list_img = file_list_img[recent_count-10:]
                
                
            img_list = []
            for file in file_list_img:
                try_count = 0
                img = None
                enc_img = b''

                while try_count < 5:
                    try:
                        with open(f'{img_file_dir}/{file}', 'rb') as f:
                            img = f.read()
                            #print(data)
                        break
                    except:
                        try_count+=1
                if img is not None:
                    enc_img = np.fromstring(img, dtype = np.uint8)
                    encoded_img = json.dumps(enc_img,cls=NumpyEncoder)
                    img_list.append({'image': encoded_img, 'imageName': file})
            return jsonify({'status': 'OK', 'images': img_list, 'fileCount': file_count})
            
        elif(recent_count == file_count):
            return jsonify({'status': 'EQ', 'msg': '업데이트할 내용이 없습니다'})
            
        elif(recent_count > file_count):
            return jsonify({'status': 'ER', 'msg': '페이지를 새로고침 해주세요.'})
        
    else: 
        return jsonify({'status': 'WR', 'msg': '이미지 경로를 찾을 수 없습니다.'})
    
app.run(host='0.0.0.0')
