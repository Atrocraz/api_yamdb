# Generated by Django 3.2 on 2023-10-26 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmation_code',
            field=models.TextField(blank=True, verbose_name='Код подтверждения'),
        ),
    ]