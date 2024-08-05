# Usa la imagen base para Python 3.6 en una arquitectura ARM 32-bits, versión Debian Buster
FROM arm64v8/python:3.7

# Establece el directorio de trabajo
WORKDIR /app

RUN pip install tflite-runtime

# Inicia una consola de Python cuando se ejecute el contenedor
CMD ["python"]
