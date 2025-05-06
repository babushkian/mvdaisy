"""
URL configuration for mvdaisy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),

    re_path('^auth/', include('djoser.urls')),
    re_path('^auth/', include('djoser.urls.authtoken')),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path('', include("main.urls", namespace="main")),
    path('experts/', include("expert.urls", namespace="experts")),
    path('users/', include("users.urls", namespace="users")),
    path('exps/', include("expertizes.urls", namespace="expertizes")),

    path('api/', include("api.urls")),



] + debug_toolbar_urls()
