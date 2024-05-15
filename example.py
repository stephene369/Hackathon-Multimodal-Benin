import subprocess

# Chemins des fichiers
video_path = "WhatsApp Video 2024-05-15 at 14.06.49.mp4"
subtitles_path = "subtitles_fon.srt"
output_path = "vide.mp4"

command = [
    "ffmpeg",
    "-i", video_path,
    "-vf", f"subtitles={subtitles_path}",
    output_path
]

# Exécuter la commande ffmpeg
subprocess.run(command, check=True)
