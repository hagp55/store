from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Customer, Image, Product, Tag


class ImagesInline(admin.TabularInline):
    model = Image
    max_num = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_select_related = ('category',)
    list_display = (
        'title',
        'category',
        'price',
        'on_sale',
        'get_preview_photo',
    )
    list_editable = (
        'on_sale',
        'price'
    )
    list_filter = (
        'category',
        'tags',
        'created_at',
    )
    search_fields = (
        'title',
    )
    fields = (
        'title',
        'description',
        'get_photo',
        'image',
        'category',
        'views_counter',
        'price',
        'slug',
        'keywords',
        'tags',
        'label',
        'on_sale',
    )
    inlines = (ImagesInline,)
    readonly_fields = (
        'get_photo',
        'views_counter',
    )
    prepopulated_fields = {
        'slug': ('title',),
    }

    @admin.display(description='Фото')
    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200px">')
        else:
            return 'Фото отсутствует'

    @admin.display(description='Миниатюра')
    def get_preview_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50px">')
        else:
            return 'Фото отсутствует'

    def get_action_choices(self, request):
        default_choices = [('', 'Выберите действие')]
        choices = super().get_action_choices(request, default_choices)
        # choices.pop(0)
        return choices

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['empty_label'] = '-Не выбрано-'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


admin.site.register(Customer)
admin.site.register(Image)
admin.site.empty_value_display = 'Не выбрано'
admin.site.site_title = settings.SITE_TITLE
admin.site.site_header = settings.SITE_HEADER
admin.site.index_title = settings.INDEX_TITLE
