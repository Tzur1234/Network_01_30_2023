# Generated by Django 4.1.5 on 2023-01-29 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_alter_user_follow_others'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
