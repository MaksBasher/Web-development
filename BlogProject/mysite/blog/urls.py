from .import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog import views

#Creating a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('api/v1/', include(router.urls), name="api"),
]