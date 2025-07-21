"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from projects.views import ProjectView
from operations.views import OperationView
from scripts.views import ScriptView
from scenes.views import SceneView
from shots.views import ShotView
from images.views import ImageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/projects", ProjectView.as_view()),
    path("api/operations", OperationView.as_view()),
    path("api/scripts", ScriptView.as_view()),
    path("api/scenes", SceneView.as_view()),
    path("api/shots", ShotView.as_view()),
    path("api/images", ImageView.as_view()),
]
