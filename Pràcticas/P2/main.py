import subprocess
from pynput import keyboard
import P1_script
import ffmpeg
import struct
import numpy as np
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt
from PIL import Image


def convert_to_mp2(input_file, output_file):
    # Convert the video to .mp2 (this will create an audio-only .mp2 file)
    conversion_command = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-c:a", "mp2",
        output_file
    ]
    subprocess.run(conversion_command)
def parse_video_info(input_file):
    # Use ffprobe to get video information
    info_command = [
        "ffprobe",
        input_file
    ]
    video_info = subprocess.check_output(info_command, stderr=subprocess.STDOUT, text=True)

    # Print the video information
    print("Video Information:")
    print(video_info)

def modify_resolution(input_file, output_file, new_width, new_height):
    # Modify the resolution of the video
    resolution_command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"scale={new_width}:{new_height}",
        output_file
    ]
    subprocess.run(resolution_command)

def change_chroma_subsampling(input_file, output_file, chroma_subsampling):
    # Change the chroma subsampling of the video
    subsampling_command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"format=yuv420p{chroma_subsampling}",
        output_file
    ]
    subprocess.run(subsampling_command)


def read_video_info(input_file):
    # Read and print relevant video information
    info_command = [
        "ffprobe",
        input_file
    ]
    video_info = subprocess.check_output(info_command, stderr=subprocess.STDOUT, text=True)

    print("Video Information:")
    lines = video_info.splitlines()
    for line in lines:
        if "Duration" in line or "Stream" in line or "Video" in line:
            print(line)

def task1():
    input_file = "/home/ubuntunil/PycharmProjects/P2/BBB.mp4"
    # Output audio-only .mp2 file
    output_file = "/home/ubuntunil/PycharmProjects/P2/BBB.mp2"
    convert_to_mp2(input_file, output_file)
    # Parse video information using ffprobe from the original .mp4 file
    parse_video_info(input_file)

def task2():
    # Prompt the user to choose a resolution
    input_file = "/home/ubuntunil/PycharmProjects/P2/BBB.mp4"
    print("Choose a resolution:")
    print("a. 480p (854x480)")
    print("b. 720p (1280x720)")
    print("c. 1080p (1920x1080)")

    resolution_choice = input("Enter the letter of your choice and press enter: ")

    if resolution_choice == "a":
        new_width, new_height = 854, 480
    elif resolution_choice == "b":
        new_width, new_height = 1280, 720
    elif resolution_choice == "c":
        new_width, new_height = 1920, 1080
    else:
        print("Invalid choice. Using default resolution (854x480).")
        new_width, new_height = 854, 480

    # Output modified resolution video
    output_file_modified_resolution = f"BBB_{new_width}x{new_height}.mp4"

    modify_resolution(input_file, output_file_modified_resolution, new_width, new_height)
    print("Modification of resolution completed")


def task3():
    input_file = "/home/ubuntunil/PycharmProjects/P2/BBB.mp4"
    # Change the chroma subsampling
    print("Choose a chroma subsampling:")
    print("1. 4:2:0 (default)")
    print("2. 4:2:2")
    print("3. 4:4:4")

    subsampling_choice = input("Enter the letter of your choice and press enter: ")

    if subsampling_choice == "e":
        chroma_subsampling = ",format=yuv422p"
    elif subsampling_choice == "f":
        chroma_subsampling = ",format=yuv444p"
    else:
        chroma_subsampling = ""

    # Output video with modified chroma subsampling
    output_file_modified_subsampling = f"BBB_subsampling{chroma_subsampling}.mp4"
    change_chroma_subsampling(input_file, output_file_modified_subsampling, chroma_subsampling)
    print("Modification of chroma subsampling completed")

def task4():
    input_file = "/home/ubuntunil/PycharmProjects/P2/BBB.mp4"
    read_video_info(input_file)

def task5():
    input_image = '/home/ubuntunil/PycharmProjects/P2/OnePiece.jpg'
    output_image = '/home/ubuntunil/PycharmProjects/P2/outputBWOnePiece.jpg'
    P1_script.transform_to_bw_and_compress(input_image, output_image)




task_mapping = {
    '1': task1,
    '2': task2,
    '3': task3,
    '4': task4,
    '5': task5,
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
        print("Press keys 1-5 to execute the tasks. Press Ctrl+C to exit")
        listener.join()

if __name__ == "__main__":
    main()



