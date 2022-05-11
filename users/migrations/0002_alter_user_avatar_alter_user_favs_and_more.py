# Generated by Django 4.0.4 on 2022-05-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20191216_0937'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favs',
            field=models.ManyToManyField(blank=True, related_name='favs', to='rooms.room'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
