# Generated by Django 3.2 on 2022-01-22 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal', '0003_auto_20220115_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recordingsession',
            old_name='Results',
            new_name='results',
        ),
    ]
