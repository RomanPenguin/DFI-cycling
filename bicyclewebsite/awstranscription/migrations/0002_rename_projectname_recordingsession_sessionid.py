# Generated by Django 3.2.9 on 2021-12-05 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awstranscription', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recordingsession',
            old_name='projectName',
            new_name='sessionID',
        ),
    ]
