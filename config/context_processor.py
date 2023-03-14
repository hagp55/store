from .settings import base


def get_context_data(request):
    context = {
        # SEO
        'title': base.title,
        'description': base.description, # Краткое описание до 140 символов
        'keywords': base.keywords, # Не больше 20 слов
        'Author': base.author,
        'Copyright': base.copyright,
        'Address': base.address,
        # Social media
        'whatsapp': base.whatsapp,
        'telegram': base.telegram,
        'vk': base.vk,
        # Contacts
        'address': base.address,
        'phone': base.phone,
        'phone_preview':base.phone_preview,
        'email': base.email,
        'map': f'{base.map}',
    }
    return context
