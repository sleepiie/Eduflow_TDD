# Generated by Django 5.1.3 on 2025-03-05 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanbanboard', '0002_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='kanbanboard.category'),
        ),
    ]
