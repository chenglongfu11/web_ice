# Generated by Django 3.0.4 on 2020-03-11 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapplication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
    ]