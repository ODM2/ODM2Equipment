from equipment_inventory.managers import SiteVisitActionManager, GenericActionManager, EquipmentDeploymentManager, \
    InstrumentDeploymentManager, InstrumentCalibrationManager, EquipmentMaintenanceManager, InstrumentRetrievalManager, \
    EquipmentRetrievalManager, RetrievalRelatedActionManager
from odm2.models import Action, RelatedAction


class SiteVisitAction(Action):
    objects = SiteVisitActionManager()

    class Meta:
        proxy = True


class GenericAction(Action):
    objects = GenericActionManager()

    class Meta:
        proxy = True


class EquipmentDeploymentAction(Action):
    objects = EquipmentDeploymentManager()

    class Meta:
        proxy = True


class InstrumentDeploymentAction(Action):
    objects = InstrumentDeploymentManager()

    class Meta:
        proxy = True


class EquipmentRetrievalAction(Action):
    objects = EquipmentRetrievalManager()

    class Meta:
        proxy = True


class InstrumentRetrievalAction(Action):
    objects = InstrumentRetrievalManager()

    class Meta:
        proxy = True


class InstrumentCalibrationAction(Action):
    objects = InstrumentCalibrationManager()

    class Meta:
        proxy = True


class EquipmentMaintenanceAction(Action):
    objects = EquipmentMaintenanceManager()

    class Meta:
        proxy = True


class RetrievalRelatedAction(RelatedAction):
    objects = RetrievalRelatedActionManager()

    class Meta:
        proxy = True
