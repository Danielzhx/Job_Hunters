# Generated by Django 5.0.4 on 2024-05-06 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('location', models.CharField(max_length=200)),
                ('due_date', models.DateField(verbose_name='Due date')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.company')),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobtype')),
            ],
        ),
    ]