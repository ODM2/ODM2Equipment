from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.db import models
from django import forms
from nested_admin.nested import NestedModelAdmin, NestedTabularInline, NestedStackedInline

from equipment_inventory.forms import SiteVisitActionForm, GenericActionForm, EquipmentDeploymentForm, \
    InstrumentDeploymentForm, ResultForm, FeatureActionForm
from equipment_inventory.models import SiteVisitAction, GenericAction, EquipmentDeploymentAction, \
    InstrumentDeploymentAction
from odm2.admin_helper import StandaloneActionAdminMixin
from odm2.models import Organization, Equipment, EquipmentModel, InstrumentOutputVariable, People, Method, Result, \
    CalibrationStandard, Site, SamplingFeature, Affiliation, FeatureAction, EquipmentUsed, ActionBy


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


@admin.register(CalibrationStandard)
class CalibrationStandardAdmin(admin.ModelAdmin):
    pass


@admin.register(EquipmentDeploymentAction)
class EquipmentDeploymentAdmin(admin.ModelAdmin):
    form = EquipmentDeploymentForm


class ResultInline(NestedTabularInline):
    initial_fields = {'result_type': 'Time series coverage'}
    model = Result
    form = ResultForm
    extra = 0
    min_num = 1


class SiteVisitFeatureActionInline(NestedStackedInline):
    model = FeatureAction
    form = FeatureActionForm
    can_delete = False
    max_num = 1


class FeatureActionInline(NestedTabularInline):
    model = FeatureAction
    inlines = [ResultInline, ]
    form = FeatureActionForm
    can_delete = False
    max_num = 1
    formfield_overrides = {
        models.ForeignKey: {'widget': forms.HiddenInput}
    }


class SingleEquipmentUsedInline(NestedStackedInline):
    model = EquipmentUsed
    can_delete = False
    max_num = 1


class ActionByInline(NestedTabularInline):
    model = ActionBy
    extra = 1


@admin.register(SiteVisitAction)
class SiteVisitActionAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = SiteVisitActionForm
    action_type = 'Field activity'
    inlines = [SiteVisitFeatureActionInline, ActionByInline]

    def save_model(self, request, obj, form, change):
        obj.method = Method.objects.get_or_create(method_type_id='Field activity', method_code='Site Visit', method_name='Site Visit')[0]
        super(SiteVisitActionAdmin, self).save_model(request, obj, form, change)


@admin.register(InstrumentDeploymentAction)
class InstrumentDeploymentAdmin(StandaloneActionAdminMixin, NestedModelAdmin):
    form = InstrumentDeploymentForm
    action_type = 'Instrument deployment'
    inlines = [SingleEquipmentUsedInline, FeatureActionInline]

    class Media:
        css = {'all': ('equipment_inventory/css/form-style.css',)}


@admin.register(GenericAction)
class GenericActionAdmin(admin.ModelAdmin):
    form = GenericActionForm


class SiteInline(admin.StackedInline):
    model = Site


@admin.register(SamplingFeature)
class SamplingFeatureAdmin(admin.ModelAdmin):
    inlines = [SiteInline, ]
    exclude = ('sampling_feature_type', )
