# Generated by Django 4.2.13 on 2025-04-13 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votoApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voto',
            name='instancia',
            field=models.CharField(default=1, max_length=24),
        ),
    ]
