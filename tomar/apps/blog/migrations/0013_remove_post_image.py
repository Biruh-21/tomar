# Generated by Django 4.0a1 on 2021-10-03 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]