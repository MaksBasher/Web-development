from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.index, name="home"),
    path("news/", views.NewsList.as_view(), name="news"),
    path('news/<slug:slug>/', views.NewsDetail.as_view(), name='news_detail'),
    path('categories/', views.category,name='categories'),
    path('categories/<slug:slug>/', views.ProductView.as_view(),name='item'),
    #path('categories/<slug:slug>/', views.item ,name='item'),
    path('tracking/', views.tracking, name='tracking'),
    path('cart/', views.cart, name="cart"),
    path('favorite/', views.favorite, name="favorite"),
    path("update_item/", views.updateItem, name="update_item"),
    path('checkout/', views.checkout, name="checkout"),
    path('process_order/', views.processOrder, name="process_order"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("profile", views.profile, name="profile"),
    path("logout", views.logout_request, name= "logout"),
    path("password/password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('test/', views.testpage, name="test"),
]