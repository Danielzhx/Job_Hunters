# Generated by Django 5.0.4 on 2024-05-08 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individual',
            name='user',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Individual',
        ),
    ]