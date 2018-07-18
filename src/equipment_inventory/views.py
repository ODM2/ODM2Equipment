from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from odm2.models import SamplingFeature, InstrumentOutputVariable


class HomeView(TemplateView):
    template_name = 'equipment_inventory/home.html'


# Site Views

class SiteListView(ListView):
    model = SamplingFeature
    template_name = 'odm2/site-list.html'
    context_object_name = 'sampling_features'


class SiteDetailView(DetailView):
    model = SamplingFeature
    template_name = 'odm2/site-detail.html'
    context_object_name = 'sampling_feature'
    slug_url_kwarg = 'sampling_feature_code'
    slug_field = 'sampling_feature_code'

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['output_variables'] = InstrumentOutputVariable.objects.filter(
            variable_id__in=self.object.actions.instrument_deployments().values_list('feature_actions__results__variable_id')
        )
        return context
