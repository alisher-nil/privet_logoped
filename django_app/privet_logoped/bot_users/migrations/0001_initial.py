# Generated by Django 4.2.15 on 2024-08-18 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True, verbose_name='ID пользователя')),
                ('role', models.CharField(choices=[('parent', 'родитель'), ('logoped', 'логопед')], max_length=100)),
                ('timezone', models.CharField(choices=[('Europe/Kaliningrad', 'Калининградское (UTC+2)'), ('Europe/Moscow', 'Московское (UTC+3)'), ('Europe/Samara', 'Самарское (UTC+4)'), ('Asia/Yekaterinburg', 'Екатеринбургское (UTC+5)'), ('Asia/Omsk', 'Омское (UTC+6)'), ('Asia/Krasnoyarsk', 'Красноярское (UTC+7)'), ('Asia/Irkutsk', 'Иркутское (UTC+8)'), ('Asia/Yakutsk', 'Якутское (UTC+9)'), ('Asia/Vladivostok', 'Владивостокское (UTC+10)'), ('Asia/Magadan', 'Магаданское (UTC+11)'), ('Asia/Kamchatka', 'Камчатское (UTC+12)')], default='Europe/Moscow', max_length=100)),
            ],
            options={
                'verbose_name': 'Пользователь Telegram',
                'verbose_name_plural': 'Пользователи Telegram',
            },
        ),
        migrations.CreateModel(
            name='VKUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True, verbose_name='ID пользователя')),
                ('role', models.CharField(choices=[('parent', 'родитель'), ('logoped', 'логопед')], max_length=100)),
                ('timezone', models.CharField(choices=[('Europe/Kaliningrad', 'Калининградское (UTC+2)'), ('Europe/Moscow', 'Московское (UTC+3)'), ('Europe/Samara', 'Самарское (UTC+4)'), ('Asia/Yekaterinburg', 'Екатеринбургское (UTC+5)'), ('Asia/Omsk', 'Омское (UTC+6)'), ('Asia/Krasnoyarsk', 'Красноярское (UTC+7)'), ('Asia/Irkutsk', 'Иркутское (UTC+8)'), ('Asia/Yakutsk', 'Якутское (UTC+9)'), ('Asia/Vladivostok', 'Владивостокское (UTC+10)'), ('Asia/Magadan', 'Магаданское (UTC+11)'), ('Asia/Kamchatka', 'Камчатское (UTC+12)')], default='Europe/Moscow', max_length=100)),
            ],
            options={
                'verbose_name': 'Пользователь VK',
                'verbose_name_plural': 'Пользователи VK',
            },
        ),
    ]
