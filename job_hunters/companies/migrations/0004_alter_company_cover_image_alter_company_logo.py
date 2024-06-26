# Generated by Django 5.0.4 on 2024-05-15 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_alter_company_cover_image_alter_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='cover_image',
            field=models.ImageField(default='default', upload_to='images/cover_images/'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default='default', upload_to='images/logo_images/'),
        ),
    ]
