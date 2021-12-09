import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from pathlib import Path
from .classifier import CutClassifier, DotClassifier
from imantics import Mask, Image, Category


class Inference(object):
    def __init__(self, config):
        self.config = config
        self.config.print()
        self.mode = config.mode
        self.save_img = config.save_img
        self.save_json = config.save_json
        self.dot_score = config.dot_score
        self.dot_pixels = config.dot_pixels
        self.dot_result_path = config.dot_result_path
        self.dot_save_path = config.dot_save_path
        self.cut_save_path = config.cut_save_path
        self.cut_model, self.dot_model = self.load_model()

    def load_model(self):
        cut_model = CutClassifier(model_name='resnet50')
        cut_model = cut_model.load_from_checkpoint(self.config.cut_model_path)
        dot_model = DotClassifier(model_name='Unet')
        dot_model = dot_model.load_from_checkpoint(self.config.dot_model_path)
        return cut_model.cuda().eval(), dot_model.cuda().eval()

    def check_tp(self, images, date):
        result = []
        annotations = []
        for i, image in enumerate(images):
            if self.find_empty(image):
                result.append(True)
                continue
            resized_image, sliced_image = self.preprocess(image)
            ### dot model processing###
            with torch.no_grad():
                mask = self.dot_model(resized_image).sigmoid()
            ### cut model processing###
            with torch.no_grad():
                logits = self.cut_model(sliced_image)

            mask[mask<self.dot_score] = 0
            mask[mask>=self.dot_score] = 1
            mask = mask.detach().cpu().numpy()
            mask = mask.squeeze().astype(np.uint8)
            mask = cv2.resize(mask, (320,80))
            pixels = np.count_nonzero(mask)

            preds = torch.argmax(logits, dim=1)
            preds = preds.detach().cpu().numpy()

            dot_result = pixels < self.dot_pixels
            cut_result = sum(preds) == 3

            if self.mode == 0:
                result.append(bool(dot_result and cut_result))
            elif self.mode == 1:
                result.append(bool(dot_result))
            else:
                result.append(bool(cut_result))
            
            if self.save_img:
                curr_time = datetime.now().strftime("%y%m%d_%H%M%S.%f").split('_')[1]
                save_path = f'{self.dot_save_path+date}/{curr_time}_{i}.png'
                result_path = f'{self.dot_result_path+date}/{curr_time}_{i}.png'
                if pixels > self.dot_pixels:
                    resized_image = resized_image.squeeze().permute(1,2,0).detach().cpu().numpy()
                    resized_image = cv2.resize(resized_image, (320,80))
                    self.result_save(result_path, resized_image, mask)
                    if self.save_json:
                        plt.imsave(save_path, image)
                        dict_anno = self.json_save(save_path, mask)
                        annotations.append(dict_anno)

                if sum(preds)!=3:
                    sliced_image = sliced_image.permute(0,2,3,1).detach().cpu().numpy()
                    for image, pred in zip(sliced_image, preds):
                        if pred == 0:
                            plt.imsave(f'{self.cut_save_path+date}/{curr_time}_{i}.png', image)
                    

        return result, annotations

    def find_empty(self, image):
        h, w, c = image.shape
        x, y = w // 2, h // 2
        center_value = image[y, x]
        if sum(center_value) < 100:
            return True
        return False

    def preprocess(self, image):
        resized_image = self.resize(image) / 255.
        resized_image = torch.Tensor(resized_image).cuda()
        resized_image = resized_image.permute(2,0,1).unsqueeze(0)

        sliced_image = self.slice_tail_head(image) / 255.
        sliced_image = torch.Tensor(sliced_image).cuda()
        sliced_image = sliced_image.permute(0,3,1,2)

        return resized_image, sliced_image
        
    def resize(self, image):
        image = cv2.resize(image, (320, 320))
        return image

    def slice_tail_head(self, image):
        ### from sliced images, divide images into head and tail
        batch = np.zeros((2,80,80,3))
        batch[0,:,:,:] = image[:,240:]
        batch[1,:,:,:] = image[:,:80]
        return batch

    def result_save(self, image_path, image, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image = cv2.drawContours(image, contours, -1, (255,0,0), 1)
        image = cv2.cvtColor(image * 255, cv2.COLOR_BGR2RGB)
        cv2.imwrite(image_path, image)

    def json_save(self, image_path, mask):
        image = Image.from_path(image_path)
        mask = Mask(mask)
        image.add(mask, category=Category('dot'))
        coco_json = image.export(style='coco')
        dic = {
                'path': coco_json['images'][0]['path'],
                'file_name':coco_json['images'][0]['file_name'],
                'annotations':coco_json['annotations'][0]['segmentation']
                }
        return dic
