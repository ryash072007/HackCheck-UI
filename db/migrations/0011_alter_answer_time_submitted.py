# Generated by Django 5.1.7 on 2025-03-12 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_hackathonsettings_max_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='time_submitted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
