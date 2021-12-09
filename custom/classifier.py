from torch import nn
from typing import Optional

import timm
import pytorch_lightning as pl
import segmentation_models_pytorch as smp


class CutClassifier(pl.LightningModule):
    def __init__(self,
                model_name='resnet18'
                ):
        super(CutClassifier, self).__init__()
        self.model = CutModel(model_name=model_name)

    def forward(self, batch):
        features = self.model(batch)
        return features

class DotClassifier(pl.LightningModule):
    def __init__(self,
                model_name=None
                ):
        super(DotClassifier, self).__init__()
        self.save_hyperparameters()
        self.model = DotModel(backbone='resnet101', model_name=model_name)

    def forward(self, batch):
        features = self.model(batch)
        return features


class CutModel(nn.Module):
    def __init__(self,
                 num_classes=3,
                 model_name='resnet18'):
        super(CutModel, self).__init__()
        self.model = timm.create_model(
            model_name, pretrained=True,
            num_classes=num_classes
            )
    
    def forward(self, x):
        features = self.model(x)
        return features


class DotModel(nn.Module):
    def __init__(self,
                 num_classes=1,
                 encoder_weights='imagenet',
                 backbone='resnet50',
                 model_name='Deeplab'):
        super(DotModel, self).__init__()
        if model_name == 'Unet':
            self.model = smp.UnetPlusPlus(encoder_name=backbone,
                                          classes=num_classes,
                                          encoder_weights=encoder_weights)
        elif model_name == 'Deeplab':
            self.model = smp.DeepLabV3Plus(encoder_name=backbone, 
                                           classes=num_classes,
                                           encoder_weights=encoder_weights)

    def forward(self, x):
        features = self.model(x)
        return features

# class Classifier(pl.LightningModule):
#     def __init__(self,
#                 model_name,
#                 num_classes,
#                 shortcut
#                 ):
#         super(Classifier, self).__init__()
#         self.save_hyperparameters()
#         if shortcut:
#             self.model = CutModel(
#                 model_name=model_name,
#                 num_classes=num_classes,
#                 )
#         else:
#             self.model = DotModel(backbone='resnet50', model_name=model_name)

#     def forward(self, batch):
#         features = self.model(batch)
#         return features

# class Model(nn.Module):
#     def __init__(self,
#                  model_name,
#                  num_classes,
#                  shortcut=False,
#                  backbone='resnet50',
#                  encoder_weights='imagenet'
#                  ):
#         super(Model, self).__init__()
#         if shortcut:
#             self.model = timm.create_model(
#                 model_name, pretrained=True,
#                 num_classes=num_classes
#             )
#         else:
#             if model_name == 'Unet':
#                 self.model = smp.UnetPlusPlus(
#                     encoder_name=backbone, classes=num_classes,
#                     encoder_weights=encoder_weights
#                     )
#             elif model_name == 'Deeplab':
#                 self.model = smp.DeepLabV3Plus(
#                     encoder_name=backbone, classes=num_classes,
#                     encoder_weights=encoder_weights
#                     )

#     def forward(self, x):
#         features = self.model(x)
#         return features
