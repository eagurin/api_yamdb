# Generated by Django 3.0.5 on 2020-10-03 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201003_1515'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together={('author', 'title')},
        ),
    ]