from django.contrib import admin
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


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    form = EquipmentForm


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    form = EquipmentModelForm


@admin.register(InstrumentOutputVariable)
class InstrumentOutputVariableAdmin(admin.ModelAdmin):
    form = InstrumentOutputVariableForm


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    form = PersonForm
    inlines = [AffiliationInline]


@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    form = MethodForm


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
    inlines = [SingleNonInstrumentEquipmentUsedInline, FeatureActionInline]


@admin.register(InstrumentDeploymentAction)
class InstrumentDeploymentAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = InstrumentDeploymentForm
    action_type = 'Instrument deployment'
    inlines = [SingleInstrumentEquipmentUsedInline, InstrumentFeatureActionInline]

    class Media:
        css = {'all': ('equipment_inventory/css/form-style.css', )}


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


@admin.register(InstrumentCalibrationAction)
class InstrumentCalibrationAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = InstrumentCalibrationForm
    action_type = 'Instrument calibration'
    inlines = [MultipleIntrumentEquipmentUsedInline, CalibrationActionInline, FeatureActionInline]


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
