# Generated by Django 3.0.5 on 2020-10-06 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Review',
        ),
    ]
