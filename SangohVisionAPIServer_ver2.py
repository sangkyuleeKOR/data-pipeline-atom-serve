from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

img_dir = '/home/bomyung/data-pipeline-atom/inference_result'
s_img_dir = '/home/bomyung/data-pipeline-atom/shortcut_result'


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
    if os.path.isdir(img_file_dir):
        file_list = os.listdir(img_file_dir)
        file_list.sort()
        file_list_img = [file for file in file_list if file.endswith('.png') or file.endswith('.jpg')]
        
        file_count = len(file_list_img)
        
        if(file_count > recent_count): 
                       
            
            # 너무많은 이미지파일 요청이 오면 안되기 때문에
            # 파일갯수가 최근 파일갯수보다 30개이상 많으면 최대 30개까지만 전송
            # 최초로 켯을때는 마지막 10개 파일만 전송
            if(30 >= file_count-recent_count and file_count != 0): 
                file_list = file_list[recent_count:]
            else: 
                file_list = file_list[recent_count-10:]
            
            file_list.sort()
                
            img_list = []
            for file in file_list:
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
            return jsonify({'status': 'EQ'})
            
        elif(recent_count > file_count):
            return jsonify({'status': 'ER', 'msg': '페이지를 새로고침 해주세요.'})
        
    else: 
        return jsonify({'status': 'WR', 'msg': '이미지 경로를 찾을 수 없습니다.'})

@app.route('/getFile2', methods=['POST'])
def getFile2():
    s_params = request.values    
    s_date = s_params['date']
    s_recent_count = int(s_params['recentCount'])
    
    s_img_file_dir = (f'{s_img_dir}/{s_date.replace("-","")}')
    
    if os.path.isdir(s_img_file_dir):
        s_file_list = os.listdir(s_img_file_dir)
        s_file_list.sort()
        s_file_list_img = [s_file for s_file in s_file_list if s_file.endswith('.png') or s_file.endswith('.jpg')]
        s_file_count = len(s_file_list_img)
        
        if(s_file_count > s_recent_count): 
            
            
            # 너무많은 이미지파일 요청이 오면 안되기 때문에
            # 파일갯수가 최근 파일갯수보다 30개이상 많으면 최대 30개까지만 전송
            # 최초로 켯을때는 마지막 10개 파일만 전송
            if(30 >= s_file_count - s_recent_count and s_file_count != 0): 
                s_file_list = s_file_list[s_recent_count:]
            else: 
                s_file_list = s_file_list[s_recent_count-10:]  
            
            s_file_list.sort()
            
            s_img_list = []
            for s_file in s_file_list:
                s_try_count = 0
                s_img = None
                s_enc_img = b''

                while s_try_count < 5:
                    try:
                        with open(f'{s_img_file_dir}/{s_file}', 'rb') as s_f:
                            s_img = s_f.read()
                            #print(data)
                        break
                    except:
                        s_try_count+=1
                if s_img is not None:
                    s_enc_img = np.fromstring(s_img, dtype = np.uint8)
                    s_encoded_img = json.dumps(s_enc_img,cls=NumpyEncoder)
                    s_img_list.append({'image': s_encoded_img, 'imageName': s_file})
            return jsonify({'status': 'OK', 'images': s_img_list, 'fileCount': s_file_count})
            
        elif(s_recent_count == s_file_count):
            return jsonify({'status': 'EQ'})
            
        elif(s_recent_count > s_file_count):
            return jsonify({'status': 'ER', 'msg': '페이지를 새로고침 해주세요.'})
        
    else: 
        return jsonify({'status': 'WR', 'msg': '이미지 경로를 찾을 수 없습니다.'})
    
app.run(host='0.0.0.0')
