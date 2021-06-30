# Generated by Django 2.1.5 on 2020-04-22 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_posting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, null=True)),
                ('size', models.CharField(max_length=4, null=True)),
                ('image', models.FileField(upload_to='')),
                ('image2', models.FileField(blank=True, upload_to='')),
                ('image3', models.FileField(blank=True, upload_to='')),
                ('image4', models.FileField(blank=True, upload_to='')),
                ('descrip', models.CharField(max_length=10000)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('designer', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('color', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('1', 'Womenswear'), ('2', 'Menswear'), ('3', 'Accesories'), ('4', 'Footwear')], max_length=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]