# Generated by Django 5.1.3 on 2025-03-08 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanbanboard', '0003_alter_topic_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('todo', 'Todo'), ('doing', 'Doing'), ('done', 'Done')], default='todo', max_length=10)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='kanbanboard.topic')),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
    ]
