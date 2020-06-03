# Generated by Django 3.0.6 on 2020-06-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='resume_email',
            field=models.EmailField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='resume_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='resume',
            name='resume_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]