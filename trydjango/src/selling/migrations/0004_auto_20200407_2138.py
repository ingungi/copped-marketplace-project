# Generated by Django 3.0.5 on 2020-04-07 21:38

from django.db import migrations, models
import selling.models


class Migration(migrations.Migration):

    dependencies = [
        ('selling', '0003_auto_20200407_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_posting',
            name='image2',
            field=models.FileField(blank=True, upload_to=selling.models.get_upload_path),
        ),
        migrations.AddField(
            model_name='item_posting',
            name='image3',
            field=models.FileField(blank=True, upload_to=selling.models.get_upload_path),
        ),
        migrations.AddField(
            model_name='item_posting',
            name='image4',
            field=models.FileField(blank=True, upload_to=selling.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='item_posting',
            name='image',
            field=models.FileField(upload_to=selling.models.get_upload_path),
        ),
    ]
