import subprocess
from pynput import keyboard
import json
import YUV
import subtitles


######Cut 9 sec of BBB###################
#ruta_video_original = '/home/ubuntunil/PycharmProjects/S2/BBB.mp4'  # Reemplaza con la ruta de tu video
#ruta_video_recortado = '/home/ubuntunil/PycharmProjects/S2/BBB_9sec.mp4'  # Ruta de destino para el video recortado
#video_original = VideoFileClip(ruta_video_original)
#video_recortado = video_original.subclip(0, 9)  # Subclip desde 0 segundos hasta 9 segundos
#video_recortado.write_videofile(ruta_video_recortado, codec='libx264', fps=24)  # Puedes ajustar el codec y la tasa de frames según tus preferencias


class VideoAnalyzer:
    def display_macroblocks_and_motion_vectors_ffplay(self, input_video_path):
        ffplay_command = [
            'ffplay',
            '-flags2', '+export_mvs',
            input_video_path,
            '-vf', 'codecview=mv=pf+bf+bb'
        ]

        subprocess.run(ffplay_command)

    def display_macroblocks_and_motion_vectors_ffmpeg(self, input_video_path, output_video_path):
        ffmpeg_command = [
            'ffmpeg',
            '-flags2', '+export_mvs',
            '-i', input_video_path,
            '-vf', 'codecview=mv=pf+bf+bb',
            output_video_path
        ]

        subprocess.run(ffmpeg_command)

class VideoAudioProcessor:
    def cut_video_segment(self, input_video, output_video_50s):
        subprocess.run(['ffmpeg', '-i', input_video, '-ss', '00:00:00', '-t', '50', '-c:v', 'copy', '-c:a', 'copy', output_video_50s])

    def extract_audio_formats(self, input_video_50s):
        subprocess.run(['ffmpeg', '-i', input_video_50s, '-vn', '-ac', '1', 'output_audio_mono.mp3'])
        subprocess.run(['ffmpeg', '-i', input_video_50s, '-vn', '-ac', '2', '-b:a', '96k', 'output_audio_stereo_low.mp3'])
        subprocess.run(['ffmpeg', '-i', input_video_50s, '-vn', '-c:a', 'aac', 'output_audio_aac.aac'])

    def package_to_mp4(self, input_video_50s, audio_mono, audio_stereo_low, audio_aac, final_output):
        subprocess.run(['ffmpeg', '-i', input_video_50s, '-i', audio_mono, '-i', audio_stereo_low, '-i', audio_aac,
                        '-map', '0:v', '-map', '1:a', '-map', '2:a', '-map', '3:a',
                        '-c:v', 'copy', '-c:a', 'copy', '-shortest', final_output])

    def count_tracks_and_formats(self, input_container):
        ffprobe_command = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            input_container
        ]

        result = subprocess.run(ffprobe_command, capture_output=True, text=True)
        output = result.stdout
        data = json.loads(output)

        num_tracks = len([stream for stream in data['streams'] if stream['codec_type'] == 'audio'])
        track_formats = [stream['codec_name'] for stream in data['streams'] if stream['codec_type'] == 'audio']

        return num_tracks, track_formats

def task1():
    video_analyzer = VideoAnalyzer()
    input_video = '/home/ubuntunil/PycharmProjects/S2/BBB_9sec.mp4'
    output_video_ffmpeg = '/home/ubuntunil/PycharmProjects/S2/BBB_MACRO_VECTORS.mp4'

    # Run ffplay command to display macroblocks and motion vectors
    video_analyzer.display_macroblocks_and_motion_vectors_ffplay(input_video)

    # Run ffmpeg command to output a video with displayed macroblocks and motion vectors
    video_analyzer.display_macroblocks_and_motion_vectors_ffmpeg(input_video, output_video_ffmpeg)

def task2():
    processor = VideoAudioProcessor()
    input_video = '/home/ubuntunil/PycharmProjects/S2/BBB.mp4'  # Replace with your input video file
    output_video_50s = '/home/ubuntunil/PycharmProjects/S2/BBB_50s.mp4'
    audio_mono = '/home/ubuntunil/PycharmProjects/S2/output_audio_mono.mp3'
    audio_stereo_low = '/home/ubuntunil/PycharmProjects/S2/output_audio_stereo_low.mp3'
    audio_aac = '/home/ubuntunil/PycharmProjects/S2/output_audio_aac.aac'
    final_output = '/home/ubuntunil/PycharmProjects/S2/output_container.mp4'


    processor.cut_video_segment(input_video, output_video_50s)

    processor.extract_audio_formats(output_video_50s)

    # Pack in a MP4
    processor.package_to_mp4(output_video_50s, audio_mono, audio_stereo_low, audio_aac, final_output)

def task3():
    processor = VideoAudioProcessor()
    input_container = '/home/ubuntunil/PycharmProjects/S2/output_container.mp4'  # Replace with your input container file

    num_tracks, track_formats = processor.count_tracks_and_formats(input_container)

    print(f"Number of tracks: {num_tracks}")
    print(f"Format of the tracks: {track_formats}")


def task4():
    print('In this task the development of the subsitles.py file is done, if you want to see the result jump to task 5')

def task5():
    video_input = '/home/ubuntunil/PycharmProjects/S2/SnapInsta.io-MARIANO RAJOY _El alcalde y el vecino_-(480p).mp4'
    sub = '/home/ubuntunil/PycharmProjects/S2/VecinoSubtitulos.srt'
    video_output = '/home/ubuntunil/PycharmProjects/S2/VecinoSUBTITULOS.mp4'
    subtitles.embed_subtitles(video_input, sub, video_output)


def task6():
    input_video = '/home/ubuntunil/PycharmProjects/S2/BBB_9sec.mp4'
    output_video = '/home/ubuntunil/PycharmProjects/S2/BBB_YUV.mp4'
    YUV.YUV_histogram(input_video,output_video)

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
        print("Press keys 1-5 to execute the tasks. Press Ctrl+C to exit")
        listener.join()

if __name__ == "__main__":
    main()




