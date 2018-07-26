from django.contrib import admin
from nested_admin.nested import NestedStackedInline, NestedTabularInline

from equipment_inventory.forms import SiteVisitFeatureActionForm, FeatureActionForm, ResultForm
from odm2.models import CalibrationAction, Site, ActionBy, EquipmentUsed, FeatureAction, Result, Affiliation, Equipment, \
    CalibrationStandard, CalibrationReferenceEquipment


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
    model = EquipmentUsed
    can_delete = False
    max_num = 1
    min_num = 1


class MultipleEquipmentUsedInline(NestedStackedInline):
    model = EquipmentUsed
    min_num = 1
    extra = 0


class ActionByInline(NestedTabularInline):
    model = ActionBy
    extra = 1


class CalibrationReferenceEquipmentInline(NestedTabularInline):
    model = CalibrationReferenceEquipment
    extra = 0


class CalibrationStandardInline(NestedTabularInline):
    model = CalibrationStandard
    extra = 0


class CalibrationActionInline(NestedStackedInline):
    inlines = [CalibrationReferenceEquipmentInline, CalibrationStandardInline]
    model = CalibrationAction
    can_delete = False


class AffiliationInline(admin.StackedInline):
    model = Affiliation
    extra = 0


class SiteInline(admin.StackedInline):
    model = Site
