# Generated by Django 4.1.7 on 2023-03-20 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_user_profile_pic_alter_shopitem_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_background',
            field=models.ForeignKey(default=71, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='profile_background', to='database.shopitem'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_border',
            field=models.ForeignKey(default=72, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='profile_border', to='database.shopitem'),
        ),
    ]
