# Generated by Django 2.1.1 on 2018-09-27 08:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(10, 'The value should be more than %(limit_value)s.')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_tittle',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(10, 'The value should be more than %(limit_value)s.')]),
        ),
    ]
