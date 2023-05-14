from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("news/", views.NewsList.as_view(), name="news"),
    path('news/<slug:slug>/', views.NewsDetail.as_view(), name='news_detail'),
    path('categories/', views.category,name='categories'),
    path('categories/<slug:slug>/', views.ProductView.as_view(),name='product'),
    path('tracking/', views.tracking, name='tracking'),
    path('cart/', views.cart, name="cart"),
    path("update_item/", views.updateItem, name="update_item"),
	path('checkout/', views.checkout, name="checkout"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
]