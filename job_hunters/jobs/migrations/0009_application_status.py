# Generated by Django 5.0.4 on 2024-05-15 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_alter_references_contact_bool'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.TextField(default='Pending', max_length=200),
        ),
    ]
