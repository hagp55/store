from django import forms


class TeleBotSendMessageForm(forms.Form):
    phone = forms.CharField()
    message = forms.CharField()