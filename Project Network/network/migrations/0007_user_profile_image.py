# Generated by Django 5.0.6 on 2024-11-22 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_image'),
        ),
    ]
