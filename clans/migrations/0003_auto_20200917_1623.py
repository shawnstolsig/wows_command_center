# Generated by Django 3.1.1 on 2020-09-17 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clans', '0002_auto_20200916_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='clan',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clan',
            name='members_count',
            field=models.IntegerField(default=0),
        ),
    ]
