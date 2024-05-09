# Generated by Django 5.0.4 on 2024-05-09 13:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individual',
            name='id',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='user',
        ),
        migrations.AddField(
            model_name='individual',
            name='owner',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]