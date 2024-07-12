Here's a step-by-step guide:

# Django Audio Downloader Project

This guide will walk you through setting up a Django project that allows users to download audio from YouTube, save it in the database, and provide a download link through the browser.

## Prerequisites

Ensure you have the following installed:
- Python
- Django
- yt-dlp
- moviepy

## 1. Setting Up the Project

### Create a Django Project

```sh
django-admin startproject audio_downloader
cd audio_downloader
```

### Create a Django App

```sh
python manage.py startapp downloader
```

### Install Required Libraries

```sh
pip install django yt-dlp moviepy
```

### Configure Installed Apps

Add the new app to your `INSTALLED_APPS` in `settings.py`.

```python
# settings.py
INSTALLED_APPS = [
    ...
    'downloader',
]
```

## 2. Create the AudioFile Model

Define a model to store audio file information.

```python
# downloader/models.py

from django.db import models

class AudioFile(models.Model):
    url = models.URLField(max_length=200)
    audio_file = models.FileField(upload_to='audios/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.audio_file.name
```

## 3. Create the Views

Create views to handle downloading, saving, and serving the audio files.

```python
# downloader/views.py

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
```

## 4. Create the HTML Template

Create an HTML template for the form where users can input a YouTube URL.

```html
<!-- downloader/templates/index.html -->

{% extends 'base.html' %}
{% block content %}
<h1>This is an audio downloader</h1>
<form action="" method="post">
    {% csrf_token %}
    <label for="video_url">Enter YouTube video URL:</label>
    <input type="text" name="video_url" id="video_url" placeholder="https://www.youtube.com/watch?v=example">
    <button type="submit">Download Audio</button>
</form>
{% if error %}
    <p>{{ error }}</p>
{% endif %}
{% if audio_file %}
    <p>Audio file saved at: <a href="{% url 'download_audio_file' audio_file.id %}" download>{{ audio_file.audio_file.name }}</a></p>
{% endif %}
{% endblock %}
```

## 5. Configure URLs

Add the necessary URL patterns to handle requests.

```python
# downloader/urls.py

from django.urls import path
from .views import index, download_audio_file

urlpatterns = [
    path('', index, name='index'),
    path('download/<int:file_id>/', download_audio_file, name='download_audio_file'),
]
```

Update the project's main `urls.py` to include the app's URLs and configure media file handling.

```python
# audio_downloader/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('downloader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 6. Configure Settings

Ensure you have media settings configured in `settings.py`.

```python
# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 7. Apply Migrations

Create and apply the migrations to set up your database schema.

```sh
python manage.py makemigrations
python manage.py migrate
```

## 8. Run the Development Server

Start the Django development server to test your application.

```sh
python manage.py runserver
```

## 9. Test Your Application

Open your browser and navigate to `http://127.0.0.1:8000/` to access the audio downloader form. Enter a YouTube URL and submit the form to download and save the audio file. You should see a link to download the saved audio file.

---
