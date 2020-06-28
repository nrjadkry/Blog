# Generated by Django 3.0.3 on 2020-06-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Theblogs', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(to='Theblogs.Categories'),
        ),
    ]
