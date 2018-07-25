from django import forms
from django.db import models
from django.views.generic.edit import ModelFormMixin
from easy_select2.widgets import Select2, Select2Multiple

from equipment_inventory.models import SiteVisitAction, GenericAction, EquipmentDeploymentAction, \
    InstrumentDeploymentAction
from odm2.models import SamplingFeature, Affiliation, Action, ActionType, Equipment, Medium, Result, Variable, Unit, \
    ProcessingLevel, FeatureAction


select_2_default_options = {
    'allowClear': True,
}


class SiteVisitActionForm(forms.ModelForm):
    class Meta:
        model = SiteVisitAction
        fields = [
            'begin_datetime',
            'begin_datetime_utc_offset',
            'end_datetime',
            'end_datetime_utc_offset',
            'action_description'
        ]


class StandaloneActionForm(forms.ModelForm):
    parent_site_visit = forms.ModelChoiceField(
        queryset=Action.objects.site_visits(),
        widget=Select2(select2attrs={'placeholder': 'Choose a Site Visit', **select_2_default_options})
    )

    def __init__(self, *args, **kwargs):
        super(StandaloneActionForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['parent_site_visit'].initial = self.instance.parent_site_visit


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


class InstrumentDeploymentForm(StandaloneActionForm):
    class Meta:
        model = InstrumentDeploymentAction
        fields = [
            'parent_site_visit',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'action_description',
            'action_file_link',
        ]
        widgets = {
            'method': Select2()
        }


class FeatureActionForm(forms.ModelForm):
    sampling_feature = forms.ModelChoiceField(queryset=SamplingFeature.objects.all(), required=False, widget=forms.HiddenInput)

    class Meta:
        model = FeatureAction
        fields = ['sampling_feature']


class SiteVisitFeatureActionForm(forms.ModelForm):
    sampling_feature = forms.ModelChoiceField(queryset=SamplingFeature.objects.all(), required=False)

    class Meta:
        model = FeatureAction
        fields = ['sampling_feature']


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