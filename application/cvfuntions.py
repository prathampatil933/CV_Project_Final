from application import app

import cv2
import numpy as np
import base64
# import matplotlib.pyplot as plt

import tensorflow as tf
from keras.utils import img_to_array, load_img
# from tensorflow import img_to_array, load_img
from keras.models import load_model
from keras.preprocessing import image

# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

from PIL import Image
import base64
import io

# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

def display(im):
    data = io.BytesIO()
    im.save(data, "JPEG")
    #Then encode the saved image file.
    encoded_img_data = base64.b64encode(data.getvalue())
    img_data = encoded_img_data.decode('utf-8')
    return img_data

def convertinit(img_data):
    img_base64 = img_data.split(",")[1]

    # Decode the base64 data
    image_bytes = base64.b64decode(img_base64)

    # Create a BytesIO object
    image_data = io.BytesIO(image_bytes)

    # Open the image with PIL
    pil_image = Image.open(image_data)
    img = np.array(pil_image)
    return img