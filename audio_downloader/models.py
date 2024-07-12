from django.db import models

class AudioFile(models.Model):
    url = models.URLField(max_length=200)
    audio_file = models.FileField(upload_to='audios/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.audio_file.name
