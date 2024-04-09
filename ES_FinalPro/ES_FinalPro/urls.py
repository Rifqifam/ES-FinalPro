from django.contrib import admin
from django.urls import path
from ES_FinalPro.api import expert_API

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', expert_API.urls)
]
