from tflite_runtime.interpreter import Interpreter, load_delegate

# Actualiza la ruta del delegado
delegate_path = '/usr/lib/aarch64-linux-gnu/libedgetpu.so.1'

print('hola')

# Ejemplo de cómo cargar el modelo con el delegado
interpreter = Interpreter(
    model_path='models/output_tflite_graph_edgetpu.tflite',
    experimental_delegates=[load_delegate(delegate_path, options={'device': 'usb'})]
)
print(' +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ')
print('INTERPRETER')
print(interpreter)
print(' +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ')