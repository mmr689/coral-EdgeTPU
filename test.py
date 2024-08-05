import numpy
import argparse
from tflite_runtime.interpreter import Interpreter, load_delegate

# Configura el analizador de argumentos
parser = argparse.ArgumentParser(description='Test script')
parser.add_argument('model_path', help='Path to the TFLite model file')
args = parser.parse_args()

print('HOLA')

# model = Interpreter(model_path=args.model_path)
model = Interpreter(args.model_path, experimental_delegates=[load_delegate('libedgetpu.so.1')])
model.allocate_tensors()
print(' +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ')
print('INTERPRETER')
print(model)
print(' +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ')

input_details = model.get_input_details()
output_details = model.get_output_details()
_, height, width, _ = input_details[0]['shape']
max_detections = output_details[0]['shape'][2]

print('Input:', height, width)
print('Output:', max_detections)

print('FIN')