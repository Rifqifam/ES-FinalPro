# Generated by Django 5.0.4 on 2024-04-09 16:39

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ChatNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=100)),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField()),
                ('chat_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_nodes', to='chatroom.chatroom')),
            ],
        ),
    ]