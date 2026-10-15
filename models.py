from django.db import models


class Resume(models.Model):
    resume = models.FileField(upload_to="resumes/")
    job_description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.resume.name