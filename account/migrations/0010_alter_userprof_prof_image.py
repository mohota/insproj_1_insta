# Generated by Django 4.0.5 on 2023-02-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_userprof_last_logedout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprof',
            name='prof_image',
            field=models.ImageField(upload_to='static/images_prof'),
        ),
    ]