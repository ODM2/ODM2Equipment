from django.contrib import admin
from nested_admin.nested import NestedModelAdmin

from equipment_inventory.admin_inlines import SiteVisitFeatureActionInline, ActionByInline, FeatureActionInline, \
    SingleEquipmentUsedInline, InstrumentFeatureActionInline, SiteInline, AffiliationInline, \
    MultipleEquipmentUsedInline, CalibrationActionInline, ReferenceMaterialValueInline
from equipment_inventory.forms import SiteVisitActionForm, GenericActionForm, EquipmentDeploymentForm, MethodForm, \
    InstrumentDeploymentForm, InstrumentCalibrationForm, SamplingFeatureForm, PersonForm, OrganizationForm, \
    ReferenceMaterialForm
from equipment_inventory.models import SiteVisitAction, GenericAction, EquipmentDeploymentAction, \
    InstrumentDeploymentAction, InstrumentCalibrationAction
from odm2.admin_helper import StandaloneActionAdminMixin
from odm2.models import Organization, Equipment, EquipmentModel, InstrumentOutputVariable, People, Method, Result, \
    CalibrationStandard, SamplingFeature, ReferenceMaterial


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationForm


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    pass


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(InstrumentOutputVariable)
class InstrumentOutputVariableAdmin(admin.ModelAdmin):
    pass


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    form = PersonForm
    inlines = [AffiliationInline]


@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    form = MethodForm


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferenceMaterial)
class ReferenceMaterialAdmin(admin.ModelAdmin):
    form = ReferenceMaterialForm
    inlines = [ReferenceMaterialValueInline]


@admin.register(SiteVisitAction)
class SiteVisitActionAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = SiteVisitActionForm
    action_type = 'Field activity'
    inlines = [SiteVisitFeatureActionInline, ActionByInline]

    def save_model(self, request, obj, form, change):
        obj.method = Method.objects.get_or_create(method_type_id='Field activity', method_code='Site Visit', method_name='Site Visit')[0]
        super(SiteVisitActionAdmin, self).save_model(request, obj, form, change)


@admin.register(EquipmentDeploymentAction)
class EquipmentDeploymentAdmin(StandaloneActionAdminMixin, admin.ModelAdmin):
    form = EquipmentDeploymentForm
    action_type = 'Equipment deployment'
    inlines = [SingleEquipmentUsedInline, FeatureActionInline]


@admin.register(InstrumentDeploymentAction)
class InstrumentDeploymentAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = InstrumentDeploymentForm
    action_type = 'Instrument deployment'
    inlines = [SingleEquipmentUsedInline, InstrumentFeatureActionInline]

    class Media:
        css = {'all': ('equipment_inventory/css/form-style.css', )}


@admin.register(InstrumentCalibrationAction)
class InstrumentCalibrationAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = InstrumentCalibrationForm
    action_type = 'Instrument calibration'
    inlines = [MultipleEquipmentUsedInline, CalibrationActionInline, FeatureActionInline]


@admin.register(GenericAction)
class GenericActionAdmin(admin.ModelAdmin):
    form = GenericActionForm


@admin.register(SamplingFeature)
class SamplingFeatureAdmin(admin.ModelAdmin):
    form = SamplingFeatureForm
    inlines = [SiteInline]
    exclude = ('sampling_feature_type', )


