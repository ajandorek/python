# Generated by Django 2.2.4 on 2020-10-12 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_auto_20201012_2300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='genres',
            new_name='genre',
        ),
    ]