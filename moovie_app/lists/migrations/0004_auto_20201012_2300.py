# Generated by Django 2.2.4 on 2020-10-12 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20201012_2226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ('id',)},
        ),
    ]
