from django.contrib import admin
from nested_admin.nested import NestedStackedInline, NestedTabularInline

from equipment_inventory.forms import SiteVisitFeatureActionForm, FeatureActionForm, ResultForm, SiteForm, ActionByForm, \
    EquipmentUsedForm, AffiliationForm, CalibrationActionForm, CalibrationReferenceEquipmentForm, \
    CalibrationStandardForm, ReferenceMaterialValueForm, FactoryServiceMaintenanceActionForm
from equipment_inventory.models import EquipmentMaintenanceAction
from odm2.models import CalibrationAction, Site, ActionBy, EquipmentUsed, FeatureAction, Result, Affiliation, Equipment, \
    CalibrationStandard, CalibrationReferenceEquipment, ReferenceMaterialValue, MaintenanceAction


class ResultInline(NestedTabularInline):
    form = ResultForm
    model = Result
    min_num = 1
    extra = 0


class FeatureActionInline(NestedStackedInline):
    form = FeatureActionForm
    model = FeatureAction
    can_delete = False
    max_num = 1


class SiteVisitFeatureActionInline(FeatureActionInline):
    form = SiteVisitFeatureActionForm


class InstrumentFeatureActionInline(FeatureActionInline):
    inlines = [ResultInline, ]


class SingleEquipmentUsedInline(NestedStackedInline):
    form = EquipmentUsedForm
    model = EquipmentUsed
    can_delete = False
    max_num = 1
    min_num = 1


class MultipleEquipmentUsedInline(NestedStackedInline):
    form = EquipmentUsedForm
    model = EquipmentUsed
    min_num = 1
    extra = 0


class ActionByInline(NestedTabularInline):
    form = ActionByForm
    model = ActionBy
    extra = 1


class CalibrationReferenceEquipmentInline(NestedTabularInline):
    form = CalibrationReferenceEquipmentForm
    model = CalibrationReferenceEquipment
    extra = 0


class CalibrationStandardInline(NestedTabularInline):
    form = CalibrationStandardForm
    model = CalibrationStandard
    extra = 0


class CalibrationActionInline(NestedStackedInline):
    inlines = [CalibrationReferenceEquipmentInline, CalibrationStandardInline]
    form = CalibrationActionForm
    model = CalibrationAction
    can_delete = False


class FactoryServiceMaintenanceInline(NestedStackedInline):
    form = FactoryServiceMaintenanceActionForm
    model = MaintenanceAction
    can_delete = False


class AffiliationInline(admin.StackedInline):
    form = AffiliationForm
    model = Affiliation
    extra = 0


class SiteInline(admin.StackedInline):
    form = SiteForm
    model = Site


class ReferenceMaterialValueInline(NestedStackedInline):
    form = ReferenceMaterialValueForm
    model = ReferenceMaterialValue
    can_delete = False
    max_num = 1
    min_num = 1
    extra = 0
