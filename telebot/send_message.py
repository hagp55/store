import requests
from django.contrib import messages

from .models import TeleBotSettings


def send_telegram(request, phone, message):
    # if TeleBotSettings.objects.get(pk=1):
    if TeleBotSettings.objects.filter(pk=1):
        telebot_settings = TeleBotSettings.objects.get(pk=1)
        token = telebot_settings.telegram_token
        chat_id = str(telebot_settings.telegram_chat_id)
        text = telebot_settings.telegram_message

        api = "https://api.telegram.org/bot"
        method = f"{api}{token}/sendMessage"

        if text.find("{") and text.find("}") and text.rfind("{") and text.rfind("}"):
            part_1 = text[0 : text.find("{")]
            part_2 = text[text.find("}") + 1 : text.rfind("{")]
            part_3 = text[text.rfind("}") : -1]

            text_slice = f"{part_1}{phone}{part_2}{message}{part_3}"
        else:
            text_slice = text
        try:
            response = requests.post(
                method,
                data={
                    "chat_id": chat_id,
                    "text": text_slice,
                },
            )
        except:
            pass
        finally:
            if response.status_code != 200:
                messages.error(request, "Ошибка отправления")
            elif response.status_code == 500:
                messages.error(request, "Ошибка отправления, проблемы на сервере")
            else:
                messages.success(request, "Сообщение доставлено, мы Вам скоро ответим!")
    else:
        messages.error(request, "Извените сервис не настроен")
