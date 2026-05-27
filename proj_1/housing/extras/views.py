from django.views.generic import TemplateView


class FAQView(TemplateView):
    template_name = "housing/faq.html"


class AboutView(TemplateView):
    template_name = "housing/about.html"
