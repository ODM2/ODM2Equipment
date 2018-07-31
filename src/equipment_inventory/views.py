from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from odm2.models import SamplingFeature, InstrumentOutputVariable, Result, Action, FeatureAction, People, Equipment, \
  ReferenceMaterialValue, EquipmentModel, Method
from equipment_inventory.models import *


class HomeView(TemplateView):
    template_name = 'equipment_inventory/home.html'


class PaginatorListView(ListView):

    default_sort_by = 'pk'
    default_per_page = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        sort_by = self.request.GET.get('sort_by', self.default_sort_by)
        page = self.request.GET.get('page', 1)
        per_page = self.request.GET.get('per_page', self.default_per_page)

        object_list = self.object_list.order_by(sort_by)
        paginator = Paginator(object_list, per_page)

        context.update(object_list=paginator.get_page(page))
        return context

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


class ActionDetailView(DetailView):
    model = Action
    template_name = 'odm2/action-detail.html'
    page_title = 'Action Detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(page_title=self.page_title)
        return context


class ActionListView(ListView):
    model = Action

    default_page_count = 25
    default_sort_order = '-begin_datetime'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        page = self.request.GET.get('page', 1)
        per_page = self.request.GET.get('per_page', self.default_page_count)
        sort_by = self.request.GET.get('sort_by', self.default_sort_order)

        actions = self.object_list.order_by(sort_by)

        paginator = Paginator(actions, per_page)
        context['actions'] = paginator.get_page(page)

        return context


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


class InstrumentDeploymentsListView(ActionListView):
    model = InstrumentDeploymentAction
    template_name = 'odm2/instrument-deployments-list.html'
    context_object_name = 'deployments'


class InstrumentDeploymentDetailView(DetailView):
    model = InstrumentDeploymentAction
    template_name = 'odm2/instrument-deployment-detail.html'
    context_object_name = 'deployment'
    slug_url_kwarg = 'action_id'
    slug_field = 'action_id'


class CalibrationActionListView(ActionListView):
    model = InstrumentCalibrationAction
    template_name = 'odm2/calibration-action-list.html'


class CalibrationActionDetailView(ActionDetailView):
    model = InstrumentCalibrationAction
    template_name = 'odm2/calibration-action-detail.html'
    page_title = 'Calibration Details'


class InstrumentRetrievalListView(ActionListView):
    model = InstrumentRetrievalAction
    template_name = 'odm2/instrument-retrievals.html'


class InstrumentRetrievalDetailView(ActionDetailView):
    model = InstrumentRetrievalAction
    template_name = 'odm2/instrument-retrieval.html'
    page_title = 'Instrument Retrieval Details'

class MethodListView(PaginatorListView):
    model = Method
    template_name = 'odm2/methods.html'
    default_sort_by = 'method_type'


class MethodDetailView(DetailView):
    model = Method
    template_name = 'odm2/method.html'
    
class CalibrationStandardsListView(ListView):
    """
    I know the class name says "CalibrationStandard" in it, but don't be fooled,
    aparently a Calibration Standard actually a Reference Material Value... ¯\_(ツ)_/¯
    """
    model = ReferenceMaterialValue
    template_name = 'odm2/calibration-standards.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        object_list = self.object_list.order_by('pk')
        paginator = Paginator(object_list, 25)

        page = self.request.GET.get('page', 1)
        context.update(object_list=paginator.get_page(page))
        return context


class CalibrationStandardDetailView(DetailView):
    model = ReferenceMaterialValue
    template_name = 'odm2/calibration-standard.html'

    
class EquipmentListView(ActionListView):
    model = Equipment
    template_name = 'odm2/equipment-list.html'
    context_object_name = 'equipments'


class EquipmentDetailView(ActionDetailView):
    model = Equipment
    template_name = 'odm2/equipment-details.html'
    page_title = 'Equipment Details'


class EquipmentModelListView(ActionListView):
    model = EquipmentModel
    template_name = 'odm2/equipment-model-list.html'


class EquipmentModelDetailView(ActionDetailView):
    model = EquipmentModel
    template_name = 'odm2/equipment-model-detail.html'
    page_title = 'Equipment Model Details'


