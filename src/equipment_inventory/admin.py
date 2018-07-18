from django.contrib import admin

# Register your models here.
from django.contrib import admin

from equipment_inventory.forms import SiteVisitActionForm, GenericActionForm, EquipmentDeploymentForm, \
    InstrumentDeploymentForm
from equipment_inventory.models import SiteVisitAction, GenericAction, EquipmentDeploymentAction, \
    InstrumentDeploymentAction
from odm2.models import Organization, Equipment, EquipmentModel, InstrumentOutputVariable, People, Method, Result, \
    CalibrationStandard, Site, SamplingFeature, Affiliation, FeatureAction


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    pass


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(InstrumentOutputVariable)
class InstrumentOutputVariableAdmin(admin.ModelAdmin):
    pass


class AffiliationInline(admin.StackedInline):
    model = Affiliation
    extra = 0


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    inlines = [AffiliationInline]


@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass


class ResultInline(admin.StackedInline):
    model = Result


@admin.register(CalibrationStandard)
class CalibrationStandardAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteVisitAction)
class SiteVisitActionAdmin(admin.ModelAdmin):
    form = SiteVisitActionForm


class FeatureActionInline(admin.StackedInline):
    model = FeatureAction


@admin.register(EquipmentDeploymentAction)
class EquipmentDeploymentAdmin(admin.ModelAdmin):
    form = EquipmentDeploymentForm


@admin.register(InstrumentDeploymentAction)
class InstrumentDeploymentAdmin(admin.ModelAdmin):
    form = InstrumentDeploymentForm
    inlines = [FeatureActionInline, ]


@admin.register(GenericAction)
class GenericActionAdmin(admin.ModelAdmin):
    form = GenericActionForm


class SiteInline(admin.StackedInline):
    model = Site


@admin.register(SamplingFeature)
class SamplingFeatureAdmin(admin.ModelAdmin):
    inlines = [SiteInline, ]
    exclude = ('sampling_feature_type', )
