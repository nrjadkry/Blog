# Generated by Django 3.0.3 on 2020-07-19 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Theblogs', '0013_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='post',
        ),
    ]