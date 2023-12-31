import os
from io import BytesIO
from urllib import request
import numpy as np
from PIL import Image
from tflite_runtime.interpreter import Interpreter

def download_image(url):
  with request.urlopen(url) as resp:
    buffer = resp.read()
  stream = BytesIO(buffer)
  img = Image.open(stream)
  return img

def prepare_image(img, target_size):
  if img.mode != 'RGB':
    img = img.convert('RGB')
  img = img.resize(target_size, Image.NEAREST)
  return img

# url = 'https://habrastorage.org/webt/rt/d9/dh/rtd9dhsmhwrdezeldzoqgijdg8a.jpeg'

def preprocess_input(url):
  img = download_image(url)
  x = prepare_image(img, (150, 150))
  x = np.array(x, dtype=np.float32)
  X = x * 1.0 / 255
  X = np.array([X])
  return X

def predict(url):
  X = preprocess_input(url)
  if os.path.exists('./bees-wasps-v2.tflite'):
    interpreter = Interpreter(model_path='bees-wasps-v2.tflite')
  else:
    interpreter = Interpreter(model_path='bees-wasps.tflite')
  interpreter.allocate_tensors()

  input_index = interpreter.get_input_details()[0]['index']
  output_index = interpreter.get_output_details()[0]['index']

  interpreter.set_tensor(input_index, X)
  interpreter.invoke()
  preds = interpreter.get_tensor(output_index)

  return dict(zip(['prob'], preds[0].tolist()))

def lambda_handler(event, context):
  url = event['url']
  preds = predict(url)
  return preds