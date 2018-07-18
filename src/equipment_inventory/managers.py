from odm2.models import *


class SiteVisitActionManager(models.Manager):
    def get_queryset(self):
        return Action.objects.site_visits()


class GenericActionManager(models.Manager):
    def get_queryset(self):
        return Action.objects.generic_actions()


class EquipmentDeploymentManager(models.Manager):
    def get_queryset(self):
        return Action.objects.equipment_deployments()


class InstrumentDeploymentManager(models.Manager):
    def get_queryset(self):
        return Action.objects.instrument_deployments()
