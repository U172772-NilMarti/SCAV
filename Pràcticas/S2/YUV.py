import subprocess


def YUV_histogram(input_video, output_video)
    command = [
        "ffmpeg",
        "-i",
        input_video,
        "-vf",
        "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay",
        "-c:a",
        "copy",
        output_video,
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video resultante guardado en: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando el comando: {e}")





