from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from odm2.models import SamplingFeature


class HomeView(TemplateView):
    template_name = 'equipment_inventory/home.html'


# Site Views

class SiteListView(ListView):
    model = SamplingFeature
    template_name = 'odm2/site_list.html'
    context_object_name = 'sampling_features'
