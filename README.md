
A continuación voy a detallar los pasos llevados a cabo para poder emplear los diferentes dispositivos Coral para la detección de objetos a partir de modelos ya preparados por Coral.

### Configuración del contenedor Docker

Para simplificar el proceso y evitar conflictos emplearemos Docker.

Una vez situados en el directorio de trabajo, empezamos:

1. Descargamos el repositorio del proyecto de Coral.

    ```bash
    git clone https://github.com/google-coral/tutorials.git
    ```

2. Nos desplazamos a la carpeta con el Dockerfile y lo construimos.

    ```bash
    cd tutorials/docker/object_detection
    docker build . -t detect-tutorial-tf1
    ```
    En este punto creamos la imagen de Docker en el sistema y le ponemos un nombre reconocible `detect-tutorial-tf1`.
    NOTA: En el servidor los comandos Docker requieren de `sudo`.

3. Definimos la carpeta del host donde encontraremos las salidas.

    ```bash
    DETECT_DIR=${PWD}/out && mkdir -p $DETECT_DIR
    ```

4. Ejecutamos el contenedor y accedemos a su consola.
    ```bash
    docker run --name edgetpu-detect \
    --rm -it --privileged -p 6006:6006 \
    --mount type=bind,src=${DETECT_DIR},dst=/tensorflow/models/research/learn_pet \
    detect-tutorial-tf1
    ```

    Importante, estamos empleando el comando `rm, eso significa que una vez salgamos del contenedor este se borrará.

### Descargar y configurar los datos de entrenamiento

Todo este proceso lo hacemos para reentrenar un modelo entrenado con COCO para que ahora sea capaz de reconocer entre perros y gatos. Los pasos de esta sección se centrarán en descargar, modificar el número de clases, 2, el *path* de los *checkpoints* y de reentrenar ya sea las últimas capas o el modelo entero.

Todo esto lo podremos hacer simplemente ejecutando el archivo `/tensorflow/models/research/learn_pet/ckpt/pipeline.config` el cuál ya viene preparado para toda esta tarea.

```bash
# Run this from within the Docker container (at tensorflow/models/research/):
./prepare_checkpoint_and_dataset.sh --network_type mobilenet_v1_ssd --train_whole_model false
```

En este punto ya hemos tomado dos decisiones:

1. El modelo a emplear, `mobilenet_v1_ssd`. También está disponible `mobilenet_v2_ssd`.
2. Que vamos a reentrenar solo las últimas capas, `train_whole_model = False`.

### Entrenamiento del modelo

Antes hemos preparado el proceso, ahora entrenamos. Según la documentación debemos definir `NUM_TRAINING_STEPS` y `NUM_EVAL_STEPS`. La documentación recomienda que si trabajamos con las últimas capas, bastaría

```bash
NUM_TRAINING_STEPS=500 && \
NUM_EVAL_STEPS=100
```

y si trabajamos con el modelo entero

```bash
NUM_TRAINING_STEPS=50000 && \
NUM_EVAL_STEPS=2000
```

Ahora ya podemos entrenar, (este proceso es lento y costoso, mi ordenador no fue capaz, el servidor IAHUB sí).

```bash
# From the /tensorflow/models/research/ directory
./retrain_detection_model.sh \
--num_training_steps ${NUM_TRAINING_STEPS} \
--num_eval_steps ${NUM_EVAL_STEPS}
```

### Compilar el modelo para ser ejecutado en la EdgeTPU de Coral

```bash
# From the Docker /tensorflow/models/research directory
./convert_checkpoint_to_edgetpu_tflite.sh --checkpoint_num 500
```
Ahora ya nos en `tutorials/docker/object_detection/out/models` los archivos resultantes.
    - `labels.txt`: Etiquetas donde 0 es el gato "Abyssinian" y 1 es el perro "american_bulldog".
    - `output_tflite_graph.tflite`: Modelo en versión TFLite.
    - `tflite_graph.pb`: Modelo Tensorflow en formato Protobuf.
    - `tflite_graph.pbtxt`: Modelo Tensorflow en formato Protobuf en forma de fichero de texto.


Ahora ya hemos terminado los pasos llevados a cabo en el contenedor Docker. Ahora pasamos a la terminal "normal".

```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
sudo apt-get install edgetpu-compiler
```

Nos aseguramos de ser adminitradores de los archivos en `out` y entramos en la carpeta `models`.

```bash
sudo chown -R $USER ${HOME}/ruta_carpetas_proyecto/tutorials/docker/object_detection/out
cd ${HOME}/ruta_carpetas_proyecto/tutorials/docker/object_detection/out/models
```

Finalmente convertimos el modelo en `.tflite` a una versión ejecutable por la EdgeTPU.

```bash
edgetpu_compiler output_tflite_graph.tflite
```

(repasar) Todo esto se encuentra en `${HOME}/ruta_carpetas_proyecto/tutorials/docker/object_detection/out/models` puede ser interesante moverlo a un lugar más cómodo con el comando `mv` (o no). Incluso lo interesante es hacerlo con github y poder ir de un lado a otro.




# Install Docker on RPi4

1. **Update your system**: Ensure that your system's package list and installed packages are up to date.
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

2. **Install Docker**: Use the following command to install Docker from the Raspberry Pi repositories.
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

3. **Add your user to the Docker group**: By adding your user to the Docker group, you can execute Docker commands without needing to use `sudo`.
   ```bash
   sudo usermod -aG docker pi
   ```

4. **Reboot or log out/in**: For the group changes to take effect, you need to reboot or log out and back in.
   ```bash
   reboot
   ```

5. **Verify Docker installation**: After rebooting, you can check if Docker is correctly installed by running:
   ```bash
   docker --version
   ```

Parece que me falta el archivo aquel para que funcione edgetpu. Mirar readme de consums