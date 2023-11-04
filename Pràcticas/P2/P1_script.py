import ffmpeg
import subprocess
import struct
from pynput import keyboard
import numpy as np
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt
from PIL import Image


def rgb_to_yuv(rgb):
    r, g, b = rgb
    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = 0.492 * (b - y)
    v = 0.877 * (r - y)
    return y, u, v


def yuv_to_rgb(yuv):
    y, u, v = yuv
    r = y + 1.13983 * v
    g = y - 0.39465 * u - 0.58060 * v
    b = y + 2.03211 * u
    return r, g, b


def resize_and_reduce_quality(input_image, output_image, width, quality):
    try:
        # Construct the FFmpeg command to resize and reduce quality
        cmd = [
            'ffmpeg',  # FFmpeg command
            '-i', input_image,  # Input image
            '-vf', f'scale={width}:-1',  # Resize to the specified width
            '-q:v', str(quality),  # Set output quality
            output_image  # Output image
        ]

        # Run the FFmpeg command
        subprocess.run(cmd, check=True)

        print(f"Resized and saved: {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Conversion failed!")


def serpentine(jpeg_file):
    try:
        with open(jpeg_file, 'rb') as file:
            jpeg_bytes = file.read()
            serpentine_values = []

            # Define the dimensions of the image in blocks
            image_width = 8  # Width in 8x8 blocks
            image_height = 8  # Height in 8x8 blocks

            # Iterate through the 8x8 blocks in the serpentine pattern
            for block_y in range(image_height):
                for block_x in range(image_width):
                    for y in range(8):
                        for x in range(8):
                            # Calculate the byte position for the current coefficient
                            byte_index = (block_x * 64 + block_y * 64 * image_width +
                                          x + y * 8) * 2
                            # Read the 16-bit coefficient (big-endian) from the JPEG data
                            value, = struct.unpack('>H', jpeg_bytes[byte_index:byte_index + 2])
                            serpentine_values.append(value)

            return serpentine_values

    except FileNotFoundError:
        print("Error: The specified JPEG file was not found.")
        return None


def transform_to_bw_and_compress(input_image, output_image):
    # Use FFMPEG to transform the image to black and white
    cmd = [
        'ffmpeg',
        '-i', input_image,  # Input image file
        '-vf', 'format=gray',  # Convert to grayscale
        '-q:v', '1',  # Set the quality for compression (lower values mean stronger compression)
        output_image
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Image {input_image} transformed to black and white and compressed at {output_image}")
    except subprocess.CalledProcessError as e:
        print(f"Error: FFMPEG returned a non-zero exit status: {e.returncode}")


def run_length_encode(data):
    encoded_data = bytearray()
    i = 0

    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            count += 1
            i += 1

        encoded_data.append(count)
        encoded_data.append(data[i])

        i += 1

    return encoded_data


def run_length_decode(encoded_data):
    decoded_data = bytearray()
    i = 0

    while i < len(encoded_data):
        count = encoded_data[i]
        value = encoded_data[i + 1]

        for _ in range(count):
            decoded_data.append(value)

        i += 2

    return decoded_data

class DCTImageCodec:
    def __init__(self, quality=95):
        self.quality = quality

    def encode(self, input_image_path, output_image_path):
        # Abre la imagen de entrada
        image = Image.open(input_image_path)

        # Convierte la imagen a escala de grises (modo 'L')
        image = image.convert('L')

        # Convierte la imagen a un arreglo numpy
        image_array = np.array(image, dtype=np.float32)

        # Realiza la Transformada Coseno Discreta (DCT) en bloques de 8x8 píxeles
        dct_matrix = np.zeros_like(image_array, dtype=np.float32)
        for i in range(0, image_array.shape[0], 8):
            for j in range(0, image_array.shape[1], 8):
                dct_matrix[i:i + 8, j:j + 8] = dct(dct(image_array[i:i + 8, j:j + 8], type=2, norm='ortho', axis=0), type=2, norm='ortho', axis=1)

        # Guarda la matriz DCT en formato de imagen
        encoded_image = Image.fromarray(dct_matrix, mode='F')
        encoded_image = encoded_image.convert('L')

        # Guarda la imagen codificada en formato JPEG
        encoded_image.save(output_image_path, format='JPEG', quality=self.quality)

    def decode(self, input_image_path, output_image_path):
        # Abre la imagen codificada
        encoded_image = Image.open(input_image_path)

        # Convierte la imagen a un arreglo numpy
        encoded_image_array = np.array(encoded_image, dtype=np.float32)

        # Realiza la Transformada Coseno Inversa Discreta (IDCT) en bloques de 8x8 píxeles
        idct_matrix = np.zeros_like(encoded_image_array, dtype=np.float32)
        for i in range(0, encoded_image_array.shape[0], 8):
            for j in range(0, encoded_image_array.shape[1], 8):
                idct_matrix[i:i + 8, j:j + 8] = idct(idct(encoded_image_array[i:i + 8, j:j + 8], type=2, norm='ortho', axis=0), type=2, norm='ortho', axis=1)

        # Escala la matriz para que los valores estén en el rango [0, 255]
        idct_matrix = np.clip(idct_matrix, 0, 255)

        # Convierte la matriz a tipo de datos entero sin signo de 8 bits
        idct_matrix = idct_matrix.astype(np.uint8)

        # Guarda la imagen decodificada en formato JPEG
        decoded_image = Image.fromarray(idct_matrix, mode='L')
        decoded_image.save(output_image_path, format='JPEG', quality=self.quality)




def task1():
    # Example RGB values (you can replace these with your values)
    rgb_values = (10, 145, 80)

    # Convert RGB to YUV
    yuv_values = rgb_to_yuv(rgb_values)

    # Convert YUV back to RGB
    converted_rgb_values = yuv_to_rgb(yuv_values)

    print(f"RGB: {rgb_values}")
    print(f"YUV: {yuv_values}")
    print(f"Converted RGB: {converted_rgb_values}")

    # Specify the input and output image paths, width, and quality


def task2():
    input_image = '/home/ubuntunil/PycharmProjects/rgb_yuv.py/Bosque.jpg'
    output_image = '/home/ubuntunil/PycharmProjects/rgb_yuv.py/output.jpg'
    width = 320
    quality = 20  # Quality value (0-31)

    # Call the method to resize and reduce the quality
    resize_and_reduce_quality(input_image, output_image, width, quality)


def task3():
    # Example usage:
    jpeg_file = '/home/ubuntunil/PycharmProjects/rgb_yuv.py/Bosque.jpg'
    serpentine_values = serpentine(jpeg_file)
    if serpentine_values:
        print(serpentine_values)


def task4():
    input_image = '/home/ubuntunil/PycharmProjects/rgb_yuv.py/OnePiece.jpg'
    output_image = '/home/ubuntunil/PycharmProjects/rgb_yuv.py/outputBWOnePiece.jpg'
    transform_to_bw_and_compress(input_image, output_image)


def task5():
    original_data = bytearray([1, 1, 1, 2, 2, 3, 3, 3, 4, 5, 5, 6, 6])
    encoded_data = run_length_encode(original_data)
    decoded_data = run_length_decode(encoded_data)

    print("Original Data:", original_data)
    print("Encoded Data:", encoded_data)
    print("Decoded Data:", decoded_data)


def task6():
    codec = DCTImageCodec(quality=95)

    # Rutas de archivo de entrada y salida
    input_image_path = "/home/ubuntunil/PycharmProjects/rgb_yuv.py/OnePiece.jpg"
    encoded_image_path = "/home/ubuntunil/PycharmProjects/rgb_yuv.py/encoded.jpg"
    decoded_image_path = "/home/ubuntunil/PycharmProjects/rgb_yuv.py/decoded.jpg"

    # Codifica la imagen6
    codec.encode(input_image_path, encoded_image_path)

    # Decodifica la imagen
    codec.decode(encoded_image_path, decoded_image_path)

    # Muestra la imagen decodificada (opcional)
    codec.encode(input_image_path, encoded_image_path)
    print('Imagen codificada guardada en:', encoded_image_path)

    # Decodifica la imagen
    codec.decode(encoded_image_path, decoded_image_path)
    print('Imagen decodificada guardada en:', decoded_image_path)


task_mapping = {
    '1': task1,
    '2': task2,
    '3': task3,
    '4': task4,
    '5': task5,
    '6': task6,
}


def on_key_release(key):
    try:
        # Obtén el nombre de la tecla presionada
        key_name = key.char
        # Verifica si la tecla presionada está en el mapeo
        if key_name in task_mapping:
            # Ejecuta la tarea correspondiente
            task_mapping[key_name]()
    except AttributeError:
        # Si no es una tecla imprimible, no hacemos nada
        pass


def main():
    # Configura el listener de teclado
    with keyboard.Listener(on_release=on_key_release) as listener:
        print("Presiona las teclas 1-6 para ejecutar las tareas. Presiona Ctrl+C para salir.")
        listener.join()


if __name__ == "__main__":
    main()
