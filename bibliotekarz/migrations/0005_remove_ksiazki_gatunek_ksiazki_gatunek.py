# Generated by Django 5.0.3 on 2024-05-10 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotekarz', '0004_gatunki_remove_ksiazki_gatunek_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ksiazki',
            name='Gatunek',
        ),
        migrations.AddField(
            model_name='ksiazki',
            name='Gatunek',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bibliotekarz.gatunki'),
            preserve_default=False,
        ),
    ]
