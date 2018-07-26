from django.db.models.expressions import F, Case, When

from odm2.models import *


class SiteVisitActionManager(models.Manager):
    def get_queryset(self):
        return Action.objects.site_visits()


class GenericActionManager(models.Manager):
    def get_queryset(self):
        return Action.objects.generic_actions().with_parent_visits()


class EquipmentDeploymentManager(models.Manager):
    def get_queryset(self):
        return Action.objects.equipment_deployments().with_parent_visits()


class InstrumentDeploymentManager(models.Manager):
    def get_queryset(self):
        return Action.objects.instrument_deployments().with_parent_visits()


class InstrumentCalibrationManager(models.Manager):
    def get_queryset(self):
        return Action.objects.instrument_calibrations().with_parent_visits()


class EquipmentMaintenanceManager(models.Manager):
    def get_queryset(self):
        return Action.objects.equipment_maintenance().with_parent_visits()
