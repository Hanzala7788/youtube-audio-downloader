# views.py

from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from .models import AudioFile
import yt_dlp
from moviepy.editor import AudioFileClip
import os
from django.conf import settings

def index(request):
    context = {}
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        audio_path = download_youtube_audio(video_url)
        if audio_path and audio_path.endswith('.mp3'):
            audio_file = save_audio_to_database(video_url, audio_path)
            if audio_file:
                context['audio_file'] = audio_file
                converted_audio_path = convert_audio_format(audio_path)
                if converted_audio_path:
                    context['converted_audio_path'] = converted_audio_path
                else:
                    context['error'] = "Error converting audio format."
                clean_up_file(audio_path)  # Clean up the intermediate mp3 file
            else:
                context['error'] = "Error saving audio to database."
        else:
            context['error'] = "Error downloading audio or wrong file format."
    return render(request, 'index.html', context)

def download_youtube_audio(url, output_path="audio.mp3"):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path.replace('.mp3', '') + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            output_file = ydl.prepare_filename(info_dict)
            base, ext = os.path.splitext(output_file)
            output_file = f"{base}.mp3"
        return output_file
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def save_audio_to_database(url, audio_path):
    try:
        audio_file = AudioFile(url=url)
        with open(audio_path, 'rb') as f:
            audio_file.audio_file.save(os.path.basename(audio_path), f, save=True)
        return audio_file
    except Exception as e:
        print(f"Error saving audio to database: {e}")
        return None

def convert_audio_format(input_path, output_path="audio.wav"):
    try:
        audio_clip = AudioFileClip(input_path)
        audio_clip.write_audiofile(output_path, codec='pcm_s16le')
        return output_path
    except Exception as e:
        print(f"Error converting audio format: {e}")
        return None

def clean_up_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning up file: {e}")

def download_audio_file(request, file_id):
    audio_file = get_object_or_404(AudioFile, id=file_id)
    file_path = audio_file.audio_file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        raise Http404("File not found")
