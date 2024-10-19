from django.contrib import admin
from django.urls import path, include  # Import 'include' here

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("quiz.urls")),  # Include the quiz app's URLs
]
