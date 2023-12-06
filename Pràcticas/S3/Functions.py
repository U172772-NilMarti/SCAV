
import easygui
from moviepy.editor import VideoFileClip, clips_array

video_path = ""
video_path2 =""
output_path = ""



def load_video():
    global video_path
    file_path = easygui.fileopenbox(filetypes=["*.mp4", "*.avi", "*.mkv", "*.flv", "*.mov", "*.wmv", "*.webm"])
    if file_path:
        video_path = file_path
        print("Loaded video:", video_path)  # Solo para comprobar en consola
        #return VideoFileClip(video_path)

def return_path():
    return video_path

def select_output_path():
    global output_path
    out_path = easygui.diropenbox(title="Seleccionar Directorio de Salida")
    if out_path:
        print("Directorio seleccionado:", out_path)  # Imprimir el directorio seleccionado
        output_path = out_path


def return_output_path():
    return output_path

import subprocess

def change_video_quality_codec(input_path, output_path, video_quality, codec_option):
    # Mapeo de las cualidades de video con sus resoluciones correspondientes
    quality_resolution_map = {
        "360p": "640x360",
        "480p": "854x480",
        "720p": "1280x720",
        "1080p": "1920x1080"
    }

    # Mapeo de los codecs de video
    codec_map = {
        "VP8": "libvpx",
        "VP9": "libvpx-vp9",
        "h265": "libx265",
        "AV1": "libaom-av1"
    }

    try:
        # Obtener la resolución correspondiente a la calidad
        resolution = quality_resolution_map.get(video_quality)

        if resolution:
            # Comando para cambiar la calidad del video con FFMPEG y establecer la tasa de bits
            subprocess.run([
                "ffmpeg", "-i", input_path, "-c:v", codec_map[codec_option], "-vf",
                f"scale={resolution}", "-b:v", "1M", "-quality", "good", "-c:a", "copy", "-f", "matroska", output_path
            ])
        else:
            print("Resolución no válida.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

def load_video_2():
    global video_path2
    file_path = easygui.fileopenbox(filetypes=["*.mp4", "*.avi", "*.mkv", "*.flv", "*.mov", "*.wmv", "*.webm"])
    if file_path:
        video_path2 = file_path
        print("Loaded video:", video_path2)  # Solo para comprobar en consola


def return_path2():
    return video_path2


def combine_videos(video_path1, video_path2, output_path):
    V1 = VideoFileClip(video_path1)
    V2 = VideoFileClip(video_path2)

    min_duration = min(V1.duration, V2.duration)
    V1 = V1.subclip(0, min_duration)
    V2 = V2.subclip(0, min_duration)

    if V1.h != V2.h:
        min_height = min(V1.h, V2.h)
        V1 = V1.crop(y1=(V1.h - min_height) // 2, y2=(V1.h + min_height) // 2)
        V2 = V2.crop(y1=(V2.h - min_height) // 2, y2=(V2.h + min_height) // 2)

    combined = clips_array([[V1, V2]])
    combined.write_videofile(output_path)
