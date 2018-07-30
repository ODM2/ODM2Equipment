from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from odm2.models import SamplingFeature, InstrumentOutputVariable, Result, Action, FeatureAction, People, Equipment
from equipment_inventory.models import *


class HomeView(TemplateView):
    template_name = 'equipment_inventory/home.html'


# Site Views

class SiteListView(ListView):
    model = SamplingFeature
    template_name = 'odm2/sites-list.html'
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


class ResultsListView(ListView):
    model = Result
    template_name = 'odm2/results-list.html'
    context_object_name = 'results'


class ResultDetailView(DetailView):
    model = Result
    template_name = 'odm2/result-detail.html'
    context_object_name = 'result'
    slug_url_kwarg = 'result_id'
    slug_field = 'result_id'


class SiteVisitListView(ListView):
    model = SiteVisitAction
    template_name = 'odm2/site-visits-list.html'
    context_object_name = 'visits'


class SiteVisitDetailView(DetailView):
    model = SiteVisitAction
    template_name = 'odm2/site-visit-detail.html'
    context_object_name = 'visit'
    slug_url_kwarg = 'action_id'
    slug_field = 'action_id'


class PeopleListView(ListView):
    model = People
    template_name = 'odm2/people-list.html'
    context_object_name = 'people'


class PeopleDetailView(DetailView):
    model = People
    template_name = 'odm2/people-detail.html'
    context_object_name = 'person'
    slug_url_kwarg = 'person_id'
    slug_field = 'person_id'



class EquipmentDeploymentsListView(ListView):
    model = EquipmentDeploymentAction
    template_name = 'odm2/equipment-deployments-list.html'
    context_object_name = 'deployments'


class EquipmentDeploymentDetailView(DetailView):
    model = EquipmentDeploymentAction
    template_name = 'odm2/equipment-deployment-detail.html'
    context_object_name = 'deployment'
    slug_url_kwarg = 'action_id'
    slug_field = 'action_id'


class InstrumentDeploymentsListView(ListView):
    model = InstrumentDeploymentAction
    template_name = 'odm2/instrument-deployments-list.html'
    context_object_name = 'deployments'


class InstrumentDeploymentDetailView(DetailView):
    model = InstrumentDeploymentAction
    template_name = 'odm2/instrument-deployment-detail.html'
    context_object_name = 'deployment'
    slug_url_kwarg = 'action_id'
    slug_field = 'action_id'

class CalibrationActionListView(ListView):
    model = InstrumentCalibrationAction
    template_name = 'odm2/calibration-action-list.html'


class CalibrationActionDetailView(DetailView):
    model = InstrumentCalibrationAction
    template_name = 'odm2/calibration-action-detail.html'

