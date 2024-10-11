from django.db import models


class TeleBotSettings(models.Model):
    telegram_token = models.CharField(
        "Telegram token",
        max_length=200,
    )
    telegram_chat_id = models.CharField(
        "Telegram chat id",
        max_length=200,
    )
    telegram_message = models.TextField("Layout message")

    class Meta:
        verbose_name = "Настройку"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return "Настройки телеграм бота. Не трогать!"
