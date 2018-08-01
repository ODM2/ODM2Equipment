from django.contrib import admin
from django.shortcuts import redirect, reverse
from equipment_inventory.admin_helpers.inlines import SiteVisitFeatureActionInline, ActionByInline, FeatureActionInline, \
    SingleEquipmentUsedInline, InstrumentFeatureActionInline, SiteInline, AffiliationInline, \
    MultipleEquipmentUsedInline, CalibrationActionInline, ReferenceMaterialValueInline, FactoryServiceMaintenanceInline, \
    RelatedDeploymentRetrievalInline, MultipleIntrumentEquipmentUsedInline, SingleInstrumentEquipmentUsedInline, \
    SingleNonInstrumentEquipmentUsedInline
from nested_admin.nested import NestedModelAdmin

from equipment_inventory.admin_helpers.helpers import StandaloneActionAdminMixin
from equipment_inventory.forms import SiteVisitActionForm, GenericActionForm, EquipmentDeploymentForm, MethodForm, \
    InstrumentDeploymentForm, InstrumentCalibrationForm, SamplingFeatureForm, PersonForm, OrganizationForm, \
    ReferenceMaterialForm, EquipmentForm, EquipmentModelForm, FactoryServiceForm, InstrumentOutputVariableForm, \
    EquipmentRetrievalForm, InstrumentRetrievalForm
from equipment_inventory.models import SiteVisitAction, GenericAction, EquipmentDeploymentAction, \
    InstrumentDeploymentAction, InstrumentCalibrationAction, EquipmentMaintenanceAction, EquipmentRetrievalAction, \
    InstrumentRetrievalAction
from odm2.models import Organization, Equipment, EquipmentModel, InstrumentOutputVariable, People, Method, Result, \
    SamplingFeature, ReferenceMaterial, Variable, Unit


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationForm

    def response_change(self, request, obj):
        return redirect(reverse('organization-details', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('organization-details', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('organization-list'))


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    form = EquipmentForm

    def response_change(self, request, obj):
        return redirect(reverse('equipment-details', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('equipment-details', kwargs={'pk': obj.pk}))


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    form = EquipmentModelForm

    def response_change(self, request, obj):
        return redirect(reverse('equipment-model-details', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('equipment-model-details', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('equipment-model-list'))


@admin.register(InstrumentOutputVariable)
class InstrumentOutputVariableAdmin(admin.ModelAdmin):
    form = InstrumentOutputVariableForm

    def response_change(self, request, obj):
        return redirect(reverse('instrument-output-variable', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('instrument-output-variable', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('instrument-output-variables'))


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    form = PersonForm
    inlines = [AffiliationInline]

    def response_change(self, request, obj):
        return redirect(reverse('people-detail', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('people-detail', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('people'))


@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    form = MethodForm

    def response_change(self, request, obj):
        return redirect(reverse('method', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('method', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('methods'))


@admin.register(ReferenceMaterial)
class ReferenceMaterialAdmin(admin.ModelAdmin):
    form = ReferenceMaterialForm
    inlines = [ReferenceMaterialValueInline]

    def response_change(self, request, obj):
        return redirect(reverse('calibration-standard', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('calibration-standard', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('calibration-standards'))


@admin.register(SiteVisitAction)
class SiteVisitActionAdmin(NestedModelAdmin, StandaloneActionAdminMixin):
    form = SiteVisitActionForm
    action_type = 'Field activity'
    inlines = [SiteVisitFeatureActionInline, ActionByInline]

    def save_model(self, request, obj, form, change):
        obj.method = Method.objects.get_or_create(method_type_id='Field activity', method_code='Site Visit', method_name='Site Visit')[0]
        super(SiteVisitActionAdmin, self).save_model(request, obj, form, change)

    def response_change(self, request, obj):
        return redirect(reverse('site-visit-detail', kwargs={'action_id': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('site-visit-detail', kwargs={'action_id': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('site-visit-list'))


@admin.register(EquipmentDeploymentAction)
class EquipmentDeploymentAdmin(StandaloneActionAdminMixin, admin.ModelAdmin):
    form = EquipmentDeploymentForm
    action_type = 'Equipment deployment'
    inlines = [SingleNonInstrumentEquipmentUsedInline, FeatureActionInline]

    def response_change(self, request, obj):
        return redirect(reverse('equipment-deployment-detail', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('equipment-deployment-detail', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('equipment-deployments-list'))


@admin.register(InstrumentDeploymentAction)
class InstrumentDeploymentAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = InstrumentDeploymentForm
    action_type = 'Instrument deployment'
    inlines = [SingleInstrumentEquipmentUsedInline, InstrumentFeatureActionInline]

    class Media:
        css = {'all': ('equipment_inventory/css/form-style.css', )}

    def response_change(self, request, obj):
        return redirect(reverse('instrument-deployment-detail', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('instrument-deployment-detail', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('instrument-deployments-list'))


@admin.register(EquipmentRetrievalAction)
class EquipmentRetrievalAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = EquipmentRetrievalForm
    action_type = 'Equipment retrieval'
    inlines = [RelatedDeploymentRetrievalInline, SingleNonInstrumentEquipmentUsedInline, FeatureActionInline]


@admin.register(InstrumentRetrievalAction)
class InstrumentRetrievalAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = InstrumentRetrievalForm
    action_type = 'Instrument retrieval'
    inlines = [RelatedDeploymentRetrievalInline, SingleInstrumentEquipmentUsedInline, FeatureActionInline]

    def response_change(self, request, obj):
        return redirect(reverse('instrument-retrieval', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('instrument-retrieval', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('instrument-retrievals'))


@admin.register(InstrumentCalibrationAction)
class InstrumentCalibrationAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = InstrumentCalibrationForm
    action_type = 'Instrument calibration'
    inlines = [MultipleIntrumentEquipmentUsedInline, CalibrationActionInline, FeatureActionInline]

    def response_change(self, request, obj):
        return redirect(reverse('calibration', kwargs={'pk': obj.pk}))

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(reverse('calibration', kwargs={'pk': obj.pk}))

    def response_delete(self, request, obj_display, obj_id):
        return redirect(reverse('calibrations'))


@admin.register(EquipmentMaintenanceAction)
class FactoryServiceAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = FactoryServiceForm
    action_type = 'Equipment maintenance'
    inlines = [SingleEquipmentUsedInline, FactoryServiceMaintenanceInline]


@admin.register(GenericAction)
class GenericActionAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = GenericActionForm
    inlines = [MultipleEquipmentUsedInline, FeatureActionInline]


@admin.register(SamplingFeature)
class SamplingFeatureAdmin(admin.ModelAdmin):
    form = SamplingFeatureForm
    inlines = [SiteInline]
