from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Customer(models.Model):
    """Model of customers"""

    MISSING_DATA = None
    MALE = 'm'
    FEMALE = 'f'

    GENDER_TYPE_CHOICES = (
        (MISSING_DATA, '---------'),
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    gender = models.CharField(
        _('Пол'), choices=GENDER_TYPE_CHOICES, max_length=1,
        blank=True, default='',
    )
    birthday_date = models.DateField(
        _('Дата рождения'), blank=True, null=True,
    )
    city = models.CharField('Населенный пункт', blank=True, max_length=255)

    class Meta:
        verbose_name = 'Покупателя'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f'Имя: ({self.user.username}) \
                Электронная почта: ({self.user.email}) \
                Телефон:({self.user.phone})'


class Category(models.Model):
    """Model of categories"""

    title = models.CharField(
        'Название', max_length=150,
    )
    slug = models.SlugField(
        'URL категории', max_length=150, unique=True,
    )
    order = models.IntegerField(
        'Порядок меню', default=1,
    )

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ('order',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        key = make_template_fragment_key('categories_list')
        cache.delete(key)
        super().save(args, kwargs)

    def get_absolute_url(self):
        return reverse('products_category', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Model of tags"""

    title = models.CharField(
        'Название', max_length=50,
    )
    slug = models.SlugField(
        'Url тэга', max_length=50, unique=True,
    )

    class Meta:
        verbose_name = 'Хэштег'
        verbose_name_plural = 'Хэштеги'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        key = make_template_fragment_key('tags_list')
        cache.delete(key)
        super().save(args, kwargs)

    def get_absolute_url(self):
        return reverse('products_tag', kwargs={'slug': self.slug})


class Product(models.Model):
    """Model of products"""

    NEW = 'n'
    SALE = 's'
    BEST = 'b'

    LABEL_TYPE_CHOICES = (
        (NEW, 'new'),
        (SALE, 'sale'),
        (BEST, 'best'),
    )
    title = models.CharField(
        'Заголовок', max_length=250, db_index=True,
    )
    description = models.TextField(
        'Описание',
    )
    image = models.ImageField(
        'Выбрать фото', upload_to='store/images/',
    )
    created_at = models.DateTimeField(
        'Создано', auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'Изменено', auto_now=True,
    )
    on_sale = models.BooleanField(
        'Показывать на сайте', default=False,
    )
    views_counter = models.IntegerField(
        'Количество просмотров', default=0,
    )
    price = models.IntegerField(
        'Цена', default=0,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='products',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name='Хэштег',
        related_name='products',
    )
    slug = models.SlugField(
        'Url для Товара', max_length=150, unique=True,
    )
    label = models.CharField(
        'Бирка', choices=LABEL_TYPE_CHOICES, max_length=1, blank=True,
    )
    keywords = models.CharField(
        'Хэштег для поисковиков', max_length=350, blank=True,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('created_at', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        categories_list_key = make_template_fragment_key('categories_list')
        tags_list_key = make_template_fragment_key('tags_list')
        cache.delete(categories_list_key)
        cache.delete(tags_list_key)
        if self.keywords is None:
            self.keywords = self.title
        if self.pk is not None:
            old_self = Product.objects.get(pk=self.pk)
            if old_self.image and self.image != old_self.image:
                old_self.image.delete(False)
        super().save(args, kwargs)

    def get_absolute_url(self):
        return reverse('single_product', kwargs={'slug': self.slug})

    @property
    def imageURL(self):
        try:
            url = self.image.url
            return url
        except:
            url = ''


class Image(models.Model):
    """Model of image gallery"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Привязка к фото',
        related_name='image_gallery',
    )
    keywords = models.CharField(
        'Хэштеги', max_length=350,
    )
    image = models.ImageField(
        'Выбрать фото', upload_to='store/images/',
    )

    class Meta:
        verbose_name = 'Фотографию для галереи изображений'
        verbose_name_plural = 'Галерея изображений'

    def __str__(self):
        return self.product.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
            return url
        except:
            url = ''
