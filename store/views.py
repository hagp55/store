from django.conf import settings
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F, Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from telebot.forms import TeleBotSendMessageForm
from telebot.send_message import send_telegram

from .models import Category, Product, Tag
from .utils import translate_search


class HomeView(ListView):
    model = Product
    paginate_by = settings.COUNT_PER_PAGE
    template_name = "store/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_obj"] = Product.objects.filter(on_sale=True).all()
        paginator = Paginator(context["page_obj"], self.paginate_by)
        page_number = self.request.GET.get("page", 1)

        try:
            context["page_obj"] = paginator.page(page_number)
        except PageNotAnInteger:
            context["page_obj"] = paginator.page(1)
        except EmptyPage:
            context["page_obj"] = paginator.page(paginator.num_pages)
        return context


class ProductsBySearchView(ListView):
    model = Product
    paginate_by = settings.COUNT_PER_PAGE
    template_name = "store/products_by_search.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.search_string = self.request.GET.get("search")
        main_search_string = translate_search(self.search_string)
        context["page_obj"] = Product.objects.filter(
            Q(title__icontains=self.search_string, on_sale=True)
            | Q(title__icontains=main_search_string, on_sale=True)
        )
        paginator = Paginator(context["page_obj"], self.paginate_by)
        page_number = self.request.GET.get("page", 1)

        try:
            context["page_obj"] = paginator.page(page_number)
        except PageNotAnInteger:
            context["page_obj"] = paginator.page(1)
        except EmptyPage:
            context["page_obj"] = paginator.page(paginator.num_pages)
        context["title"] = str(self.search_string)
        context["search"] = f'search={self.request.GET.get("search")}&'
        return context


class ProductsByCategoryView(ListView):
    allow_empty = False
    model = Product
    paginate_by = settings.COUNT_PER_PAGE
    template_name = "store/products_by_category.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["page_obj"] = Product.objects.filter(
            category__slug=self.kwargs["slug"], on_sale=True
        )
        paginator = Paginator(context["page_obj"], self.paginate_by)
        page_number = self.request.GET.get("page", 1)

        try:
            context["page_obj"] = paginator.page(page_number)
        except PageNotAnInteger:
            context["page_obj"] = paginator.page(1)
        except EmptyPage:
            context["page_obj"] = paginator.page(paginator.num_pages)
        context["title"] = f'{Category.objects.get(slug=self.kwargs["slug"])}'
        return context


class ProductsByTagsView(ListView):
    allow_empty = False
    model = Product
    paginate_by = settings.COUNT_PER_PAGE
    template_name = "store/products_by_tags.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["page_obj"] = Product.objects.filter(
            tags__slug=self.kwargs["slug"], on_sale=True
        )
        paginator = Paginator(context["page_obj"], self.paginate_by)
        page_number = self.request.GET.get("page", 1)

        try:
            context["page_obj"] = paginator.page(page_number)
        except PageNotAnInteger:
            context["page_obj"] = paginator.page(1)
        except EmptyPage:
            context["page_obj"] = paginator.page(paginator.num_pages)

        context["title"] = f'{Tag.objects.get(slug=self.kwargs["slug"])}'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        self.object.views_counter = F("views_counter") + 1
        self.object.save()
        self.object.refresh_from_db()
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(
            on_sale=True,
            tags__in=self.object.tags.all(),
        )
        context["image_gallery"] = self.object.image_gallery.all()
        return context


def contacts(request):
    if request.method == "POST":
        form = TeleBotSendMessageForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]
            clean_phone = (
                phone.replace(" ", "")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
            )
            if phone[0] == "+" and clean_phone[1:].isdigit():
                send_telegram(request, clean_phone, message)
            else:
                messages.error(request, "Телефон должен содержать только цифры")
        else:
            messages.error(request, "Заполните все поля")
    form = TeleBotSendMessageForm()
    context = {"form": form}
    return render(request, "store/contact.html", context)
