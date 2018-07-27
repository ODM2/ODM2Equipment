from django.db import models

from odm2.models import Action, RelatedAction


# ACTIONS

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


class EquipmentRetrievalManager(models.Manager):
    def get_queryset(self):
        return Action.objects.equipment_retrievals().with_parent_visits()


class InstrumentRetrievalManager(models.Manager):
    def get_queryset(self):
        return Action.objects.instrument_retrievals().with_parent_visits()


class InstrumentCalibrationManager(models.Manager):
    def get_queryset(self):
        return Action.objects.instrument_calibrations().with_parent_visits()


class EquipmentMaintenanceManager(models.Manager):
    def get_queryset(self):
        return Action.objects.equipment_maintenance().with_parent_visits()


# RELATED ACTIONS

class RetrievalRelatedActionManager(models.Manager):
    def get_queryset(self):
        return RelatedAction.objects.retrieval_relationships()
