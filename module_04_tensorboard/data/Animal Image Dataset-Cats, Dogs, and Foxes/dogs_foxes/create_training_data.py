import numpy as np
import pickle
import random
import os
from tqdm import tqdm
import cv2

layer_01 = [1, 2, 3]
layer_02 = [11, 12, 13]
layer_03 = [21, 22, 23]

for layer_1 in layer_01:
    for layer_2 in layer_02:
        for layer_3 in layer_03:
            print (f"Processing combination: {layer_1}, {layer_2}, {layer_3}")

