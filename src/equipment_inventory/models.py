from equipment_inventory.managers import SiteVisitActionManager, GenericActionManager, EquipmentDeploymentManager, \
    InstrumentDeploymentManager, InstrumentCalibrationManager
from odm2.models import Action


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


class InstrumentCalibrationAction(Action):
    objects = InstrumentCalibrationManager()

    class Meta:
        proxy = True
