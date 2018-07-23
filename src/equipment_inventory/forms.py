from django import forms
from django.db import models
from easy_select2.widgets import Select2, Select2Multiple

from equipment_inventory.models import SiteVisitAction, GenericAction, EquipmentDeploymentAction, \
    InstrumentDeploymentAction
from odm2.models import SamplingFeature, Affiliation, Action, ActionType, Equipment, Medium, Result, Variable, Unit, \
    ProcessingLevel, FeatureAction


select_2_default_options = {
    'allowClear': True,
}


class SiteVisitActionForm(forms.ModelForm):
    sampling_feature = forms.ModelChoiceField(
        label='Site',
        queryset=SamplingFeature.objects.all(),
        widget=Select2(select2attrs={'placeholder': 'Choose a Site', **select_2_default_options}),
    )
    people = forms.ModelMultipleChoiceField(
        label='Crew',
        queryset=Affiliation.objects.all(),
        widget=Select2Multiple(select2attrs={'placeholder': 'Select the crew members'}),
    )

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
    site_visit = forms.ModelChoiceField(
        queryset=Action.objects.site_visits(),
        widget=Select2(select2attrs={'placeholder': 'Choose a Site Visit', **select_2_default_options})
    )
    action_type = forms.ModelChoiceField(
        queryset=ActionType.objects.generic_action_types(),
        widget=Select2(select2attrs={'placeholder': 'Choose the action type (or not.)', **select_2_default_options})
    )

    equipment_used = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        widget=Select2Multiple(select2attrs={'placeholder': 'Choose the equipment used in this deployment'})
    )

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
    site_visit = forms.ModelChoiceField(
        queryset=Action.objects.site_visits(),
        widget=Select2(select2attrs={'placeholder': 'Choose a Site Visit', **select_2_default_options})
    )
    equipment_used = forms.ModelChoiceField(
        queryset=Equipment.objects.non_instruments(),
        widget=Select2(select2attrs={'placeholder': 'Choose the equipment used in this deployment', **select_2_default_options})
    )

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
    site_visit = forms.ModelChoiceField(
        queryset=Action.objects.site_visits(),
        widget=Select2(select2attrs={'placeholder': 'Choose a Site Visit', **select_2_default_options})
    )
    equipment_used = forms.ModelChoiceField(
        queryset=Equipment.objects.instruments(),
        widget=Select2(select2attrs={'placeholder': 'Choose the equipment used in this deployment', **select_2_default_options})
    )

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


class FeatureActionForm(forms.ModelForm):
    class Meta:
        model = FeatureAction
        fields = []


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            'variable',
            'unit',
            'processing_level',
            'sampled_medium',
        ]
        widgets = {
            'variable': Select2(select2attrs={'placeholder': 'Choose the variable', **select_2_default_options}),
            'unit': Select2(select2attrs={'placeholder': 'Choose the units', **select_2_default_options}),
            'processing_level': Select2(select2attrs={'placeholder': 'Choose the processing level', **select_2_default_options}),
            'sampled_medium': Select2(select2attrs={'placeholder': 'Choose the sampled medium', **select_2_default_options})
        }