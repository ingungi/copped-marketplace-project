# Generated by Django 3.0.5 on 2020-04-15 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selling', '0005_auto_20200415_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_posting',
            name='size',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='item_posting',
            name='title',
            field=models.CharField(max_length=25, null=True),
        ),
    ]