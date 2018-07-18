from django import forms
from django.db import models
from easy_select2.widgets import Select2, Select2Multiple

from equipment_inventory.models import SiteVisitAction, GenericAction, EquipmentDeploymentAction, \
    InstrumentDeploymentAction
from odm2.models import SamplingFeature, Affiliation, Action, ActionType, Equipment


class SiteVisitActionForm(forms.ModelForm):
    sampling_feature = forms.ModelChoiceField(queryset=SamplingFeature.objects.all(), widget=Select2(), label='Site')
    people = forms.ModelMultipleChoiceField(queryset=Affiliation.objects.all(), widget=Select2Multiple(), label='Crew')

    class Meta:
        model = SiteVisitAction
        fields = [
            'sampling_feature',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'end_datetime',
            'end_datetime_utc_offset',
            'action_description',
            'people'
        ]


class GenericActionForm(forms.ModelForm):
    site_visit = forms.ModelChoiceField(queryset=Action.objects.site_visits(), widget=Select2())
    action_type = forms.ModelChoiceField(queryset=ActionType.objects.generic_action_types(), widget=Select2())
    equipment_used = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all(), widget=Select2Multiple())

    class Meta:
        model = GenericAction
        fields = [
            'site_visit',
            'action_type',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'end_datetime',
            'end_datetime_utc_offset',
            'action_description',
            'action_file_link',
            'equipment_used'
        ]
        widgets = {
            'method': Select2()
        }


class EquipmentDeploymentForm(forms.ModelForm):
    site_visit = forms.ModelChoiceField(queryset=Action.objects.site_visits(), widget=Select2())
    equipment_used = forms.ModelChoiceField(queryset=Equipment.objects.non_instruments(), widget=Select2())

    class Meta:
        model = EquipmentDeploymentAction
        fields = [
            'site_visit',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'action_description',
            'action_file_link',
            'equipment_used'
        ]
        widgets = {
            'method': Select2()
        }


class InstrumentDeploymentForm(forms.ModelForm):
    site_visit = forms.ModelChoiceField(queryset=Action.objects.site_visits(), widget=Select2())
    equipment_used = forms.ModelChoiceField(queryset=Equipment.objects.instruments(), widget=Select2())

    class Meta:
        model = InstrumentDeploymentAction
        fields = [
            'site_visit',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'action_description',
            'action_file_link',
            'equipment_used'
        ]
        widgets = {
            'method': Select2()
        }
