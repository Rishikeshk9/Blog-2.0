# Generated by Django 2.2.5 on 2019-09-25 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190924_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='visit',
        ),
    ]
