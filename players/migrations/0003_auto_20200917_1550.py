# Generated by Django 3.1.1 on 2020-09-17 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_auto_20200916_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='joined_at',
            new_name='joined_clan_at',
        ),
    ]
