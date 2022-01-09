# Generated by Django 3.2 on 2022-01-09 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=200)),
                ('recordedTime', models.DateTimeField(verbose_name='date recorded')),
                ('media', models.FileField(blank=True, null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='Fitbit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=200)),
                ('recordedTime', models.DateTimeField(verbose_name='date recorded')),
                ('media', models.FileField(blank=True, null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='GPS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=200)),
                ('recordedTime', models.DateTimeField(verbose_name='date recorded')),
                ('media', models.FileField(blank=True, null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='HRV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=200)),
                ('recordedTime', models.DateTimeField(verbose_name='date recorded')),
                ('media', models.FileField(blank=True, null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='SkinConductance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=200)),
                ('recordedTime', models.DateTimeField(verbose_name='date recorded')),
                ('media', models.FileField(blank=True, null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='VideoInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=200)),
                ('recordedTime', models.DateTimeField(verbose_name='date recorded')),
                ('media', models.FileField(blank=True, null=True, upload_to='media')),
            ],
        ),
        migrations.CreateModel(
            name='RecordingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionID', models.CharField(max_length=200)),
                ('participantID', models.CharField(max_length=200)),
                ('audioInput', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dataportal.audioinput')),
                ('fitbit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dataportal.fitbit')),
                ('gPS', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dataportal.gps')),
                ('hRV', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dataportal.hrv')),
                ('skinConductance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dataportal.skinconductance')),
                ('videoInput', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dataportal.videoinput')),
            ],
        ),
    ]