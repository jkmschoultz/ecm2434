# Generated by Django 4.1.7 on 2023-03-19 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_merge_20230319_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingFriendInvite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('potentialFriend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='potentialFriend', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
