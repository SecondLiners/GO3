# Generated by Django 3.0.7 on 2020-09-12 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_remove_memberpreferences_show_long_agenda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='is_active',
        ),
    ]