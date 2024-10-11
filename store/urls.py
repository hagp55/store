from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("search/", views.ProductsBySearchView.as_view(), name="search"),
    path(
        "category/<slug>",
        views.ProductsByCategoryView.as_view(),
        name="products_category",
    ),
    path("detail/<slug>", views.ProductDetailView.as_view(), name="single_product"),
    path("tag/<slug>/", views.ProductsByTagsView.as_view(), name="products_tag"),
    path("contacts/", views.contacts, name="contacts"),
]
