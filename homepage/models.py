from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    post_tittle = models.CharField(
        validators=[MinLengthValidator(10, "The value should be more than %(limit_value)s.")], max_length=200)
    post_date = models.DateTimeField()
    post_content = models.CharField(
        validators=[MinLengthValidator(10, "The value should be more than %(limit_value)s.")], max_length=500)
    post_key = models.CharField(max_length=200)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.post_tittle
