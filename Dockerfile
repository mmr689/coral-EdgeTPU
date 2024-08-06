# Usa la imagen base para Python 3.7 en una arquitectura ARM 64-bits, versión Debian Buster
FROM arm64v8/python:3.8

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias necesarias para apt-get y wget
RUN apt-get update && apt-get install -y wget

# Descarga el paquete libedgetpu y lo instala
RUN wget https://github.com/feranick/libedgetpu/releases/download/v16.0TF2.15.1-1/libedgetpu1-std_16.0tf2.15.1-1.bookworm_arm64.deb
RUN apt-get install -y ./libedgetpu1-std_16.0tf2.15.1-1.bookworm_arm64.deb

# Crea un script para configurar LD_LIBRARY_PATH y luego iniciar bash
RUN echo "#!/bin/bash\nexport LD_LIBRARY_PATH=/usr/lib/aarch64-linux-gnu:\$LD_LIBRARY_PATH\nexec \"/bin/bash\"" > /start.sh
RUN chmod +x /start.sh

# Instala tflite-runtime
RUN pip install tflite-runtime

# Inicia una consola de Python cuando se ejecute el contenedor
CMD ["/bin/bash"]
