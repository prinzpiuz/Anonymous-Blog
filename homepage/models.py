from django.db import models


# Create your models here.


class Post(models.Model):
    post_tittle = models.CharField(max_length=200)
    post_date = models.DateTimeField()
    post_content = models.CharField(max_length=500)
    post_key = models.CharField(max_length=200)

    def __str__(self):
        return self.id
