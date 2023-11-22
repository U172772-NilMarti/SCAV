import subprocess

def embed_subtitles(video_input, subtitulos, video_output):
    comando_ffmpeg = [
        'ffmpeg',
        '-i', video_input,
        '-i', subtitulos,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-c:s', 'mov_text',
        video_output
    ]

    proceso = subprocess.Popen(comando_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, errores = proceso.communicate()

    if proceso.returncode == 0:
        print('Subtitles embed correctly.')
    else:
        print(f'ERROR OCCURRED: {errores.decode("utf-8")}')


