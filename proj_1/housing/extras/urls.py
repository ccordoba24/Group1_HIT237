from django.urls import path

from .views import FAQView, AboutView

urlpatterns = [
    path("faq/", FAQView.as_view(), name="faq"),
    path("about/", AboutView.as_view(), name="about"),
]
