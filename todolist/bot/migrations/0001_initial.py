# Generated by Django 4.0.1 on 2023-01-09 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_chat_id', models.BigIntegerField()),
                ('tg_user_id', models.BigIntegerField(unique=True)),
                ('tg_username', models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(5)])),
                ('verification_code', models.CharField(max_length=10, unique=True)),
            ],
        ),
    ]
