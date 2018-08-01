from django import forms
from django.db import models
from django.views.generic.edit import ModelFormMixin
from easy_select2.widgets import Select2, Select2Multiple

from equipment_inventory.models import SiteVisitAction, GenericAction, EquipmentDeploymentAction, \
    InstrumentDeploymentAction, InstrumentCalibrationAction, InstrumentRetrievalAction, \
    EquipmentRetrievalAction, RetrievalRelatedAction
from odm2.models import SamplingFeature, Affiliation, Action, ActionType, Equipment, Medium, Result, Variable, Unit, \
    ProcessingLevel, FeatureAction, Method, CalibrationAction, Model, Site, ActionBy, EquipmentUsed, People, \
    Organization, CalibrationReferenceEquipment, CalibrationStandard, ReferenceMaterial, ReferenceMaterialValue, \
    EquipmentModel, MaintenanceAction, InstrumentOutputVariable, RelatedAction

from django.contrib.admin.widgets import AdminDateWidget;

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
        begin_datetime_utc_offset = forms.NumberInput()
        end_datetime_utc_offset = forms.NumberInput()


class StandaloneActionForm(forms.ModelForm):
    parent_site_visit = forms.ModelChoiceField(
        queryset=Action.objects.site_visits(),
        widget=Select2(select2attrs={'placeholder': 'Choose a Site Visit', **select_2_default_options})
    )

    def __init__(self, *args, **kwargs):
        super(StandaloneActionForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['parent_site_visit'].initial = self.instance.parent_site_visit


class GenericActionForm(StandaloneActionForm):
    action_type = forms.ModelChoiceField(
        queryset=ActionType.objects.generic_action_types(),
        widget=Select2(select2attrs={'placeholder': 'Choose the action type (or not.)', **select_2_default_options})
    )
    method = forms.ModelChoiceField(
        queryset=Method.objects.generic_action_methods(),
        widget=Select2(
            select2attrs={'placeholder': 'Choose the instrument calibration method', **select_2_default_options})
    )

    class Meta:
        model = GenericAction
        fields = [
            'parent_site_visit',
            'action_type',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'end_datetime',
            'end_datetime_utc_offset',
            'action_description',
            'action_file_link'
        ]


class InstrumentCalibrationForm(StandaloneActionForm):
    method = forms.ModelChoiceField(
        queryset=Method.objects.instrument_calibration_methods(),
        widget=Select2(
            select2attrs={'placeholder': 'Choose the instrument calibration method', **select_2_default_options})
    )

    class Meta:
        model = InstrumentCalibrationAction
        fields = [
            'parent_site_visit',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'end_datetime',
            'end_datetime_utc_offset',
            'action_description',
            'action_file_link'
        ]


class EquipmentDeploymentForm(StandaloneActionForm):
    method = forms.ModelChoiceField(
        queryset=Method.objects.equipment_deployment_methods(),
        widget=Select2(
            select2attrs={'placeholder': 'Choose the equipment deployment method', **select_2_default_options})
    )

    class Meta:
        model = EquipmentDeploymentAction
        fields = [
            'parent_site_visit',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'action_description',
            'action_file_link'
        ]


class FactoryServiceForm(forms.ModelForm):
    method = forms.ModelChoiceField(
        queryset=Method.objects.equipment_maintenance_methods(),
        widget=Select2(
            select2attrs={'placeholder': 'Choose the equipment maintenance method', **select_2_default_options})
    )

    class Meta:
        model = EquipmentDeploymentAction
        fields = [
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'end_datetime',
            'end_datetime_utc_offset',
            'action_description',
            'action_file_link'
        ]


class InstrumentDeploymentForm(StandaloneActionForm):
    method = forms.ModelChoiceField(
        queryset=Method.objects.instrument_deployment_methods(),
        widget=Select2(select2attrs={'placeholder': 'Choose the instrument deployment method', **select_2_default_options})
    )

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


class RelatedDeploymentRetrievalForm(forms.ModelForm):
    related_action = forms.ModelChoiceField(
        queryset=Action.objects.deployments(),
        widget=Select2(select2attrs={'placeholder': 'Choose the deployment', **select_2_default_options}),
        label='Deployment'
    )

    class Meta:
        model = RetrievalRelatedAction
        exclude = ['relationship_type']


class EquipmentRetrievalForm(StandaloneActionForm):
    method = forms.ModelChoiceField(
        queryset=Method.objects.equipment_retrieval_methods(),
        widget=Select2(select2attrs={'placeholder': 'Choose the equipment retrieval method', **select_2_default_options})
    )

    class Meta:
        model = EquipmentRetrievalAction
        fields = [
            'parent_site_visit',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'action_description',
            'action_file_link',
        ]


class InstrumentRetrievalForm(StandaloneActionForm):
    method = forms.ModelChoiceField(
        queryset=Method.objects.instrument_retrieval_methods(),
        widget=Select2(select2attrs={'placeholder': 'Choose the instrument retrieval method', **select_2_default_options})
    )

    class Meta:
        model = InstrumentRetrievalAction
        fields = [
            'parent_site_visit',
            'method',
            'begin_datetime',
            'begin_datetime_utc_offset',
            'action_description',
            'action_file_link',
        ]


class FeatureActionForm(forms.ModelForm):
    sampling_feature = forms.ModelChoiceField(queryset=SamplingFeature.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta:
        model = FeatureAction
        fields = ['sampling_feature']


class SiteVisitFeatureActionForm(forms.ModelForm):
    sampling_feature = forms.ModelChoiceField(
        queryset=SamplingFeature.objects.all(),
        required=False,
        widget=Select2(select2attrs={'placeholder': 'Choose the site', **select_2_default_options})
    )

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


class SamplingFeatureForm(forms.ModelForm):
    class Meta:
        model = SamplingFeature
        fields = '__all__'
        widgets = {
            'sampling_feature_geo_type': Select2(select2attrs={'placeholder': 'Choose the site\'s geo-type', **select_2_default_options}),
            'elevation_datum': Select2(select2attrs={'placeholder': 'Choose the elevation datum', **select_2_default_options}),
        }


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        widgets = {
            'site_type': Select2(select2attrs={'placeholder': 'Choose the site type', **select_2_default_options}),
            'spatial_reference': Select2(select2attrs={'placeholder': 'Choose the spatial reference', **select_2_default_options})
        }


class MethodForm(forms.ModelForm):
    class Meta:
        model = Method
        fields = '__all__'
        widgets = {
            'method_type': Select2(select2attrs={'placeholder': 'Choose the method type', **select_2_default_options}),
            'organization': Select2(select2attrs={'placeholder': 'Choose the organization', **select_2_default_options}),
        }


class ActionByForm(forms.ModelForm):
    class Meta:
        model = ActionBy
        fields = '__all__'
        widgets = {
            'affiliation': Select2(select2attrs={'placeholder': 'Choose the affiliated person', **select_2_default_options}),
        }


class CalibrationActionForm(forms.ModelForm):
    class Meta:
        model = CalibrationAction
        fields = '__all__'
        widgets = {
            'instrument_output_variable': Select2(select2attrs={'placeholder': 'Choose the instrument output variable', **select_2_default_options}),
        }


class FactoryServiceMaintenanceActionForm(forms.ModelForm):
    class Meta:
        model = MaintenanceAction
        exclude = ['is_factory_service']


class InstrumentEquipmentUsedForm(forms.ModelForm):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.instruments(),
        widget=Select2(select2attrs={'placeholder': 'Choose the equipment used', **select_2_default_options})
    )

    class Meta:
        model = EquipmentUsed
        fields = ['equipment']


class NonInstrumentEquipmentUsedForm(forms.ModelForm):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.non_instruments(),
        widget=Select2(select2attrs={'placeholder': 'Choose the equipment used', **select_2_default_options})
    )

    class Meta:
        model = EquipmentUsed
        fields = ['equipment']


class EquipmentUsedForm(forms.ModelForm):
    class Meta:
        model = EquipmentUsed
        fields = ['equipment']
        widgets = {
            'equipment': Select2(select2attrs={'placeholder': 'Choose the equipment used', **select_2_default_options}),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = People
        fields = '__all__'


class AffiliationForm(forms.ModelForm):
    class Meta:
        model = Affiliation
        fields = '__all__'
        widgets = {
            'organization': Select2(select2attrs={'placeholder': 'Choose the affliated organization', **select_2_default_options}),
        }


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {
            'organization_type': Select2(select2attrs={'placeholder': 'Choose the organization type', **select_2_default_options}),
            'parent_organization': Select2(select2attrs={'placeholder': 'Choose the parent organization', **select_2_default_options}),
        }


class CalibrationReferenceEquipmentForm(forms.ModelForm):
    class Meta:
        model = CalibrationReferenceEquipment
        fields = '__all__'
        widgets = {
            'equipment': Select2(select2attrs={'placeholder': 'Choose the reference equipment', **select_2_default_options}),
        }


class CalibrationStandardForm(forms.ModelForm):
    class Meta:
        model = CalibrationStandard
        fields = ['reference_material']
        widgets = {
            'reference_material': Select2(select2attrs={'placeholder': 'Choose the reference material', **select_2_default_options}),
        }


class ReferenceMaterialForm(forms.ModelForm):
    class Meta:
        model = ReferenceMaterial
        exclude = ['reference_material_expiration_date', 'sampling_feature', 'external_identifiers']
        widgets = {
            'reference_material_medium': Select2(select2attrs={'placeholder': 'Choose the medium', **select_2_default_options}),
            'reference_material_organization': Select2(select2attrs={'placeholder': 'Choose the organization ', **select_2_default_options}),
        }


class ReferenceMaterialValueForm(forms.ModelForm):
    class Meta:
        model = ReferenceMaterialValue
        exclude = ['citation']
        widgets = {
            'variable': Select2(select2attrs={'placeholder': 'Choose the variable', **select_2_default_options}),
            'unit': Select2(select2attrs={'placeholder': 'Choose the units', **select_2_default_options}),
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'equipment_type': Select2(select2attrs={'placeholder': 'Choose the equipment type', **select_2_default_options}),
            'equipment_model': Select2(select2attrs={'placeholder': 'Choose the equipment model', **select_2_default_options}),
            'equipment_owner': Select2(select2attrs={'placeholder': 'Choose the owner', **select_2_default_options}),
            'equipment_vendor': Select2(select2attrs={'placeholder': 'Choose the vendor', **select_2_default_options}),
        }


class EquipmentModelForm(forms.ModelForm):
    class Meta:
        model = EquipmentModel
        fields = '__all__'
        widgets = {
            'model_manufacturer': Select2(select2attrs={'placeholder': 'Choose the model manufacturer', **select_2_default_options}),
        }


class InstrumentOutputVariableForm(forms.ModelForm):
    class Meta:
        model = InstrumentOutputVariable
        fields = '__all__'
        widgets = {
            'model': Select2(select2attrs={'placeholder': 'Choose the model', **select_2_default_options}),
            'variable': Select2(select2attrs={'placeholder': 'Choose the variable', **select_2_default_options}),
            'instrument_method': Select2(select2attrs={'placeholder': 'Choose the method', **select_2_default_options}),
            'instrument_raw_output_unit': Select2(select2attrs={'placeholder': 'Choose the units', **select_2_default_options}),
        }
