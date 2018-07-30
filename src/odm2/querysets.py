import datetime
from django.db import models

# region ODM2 Core models
from django.db.models.expressions import OuterRef, Subquery, F
from django.db.models.query import Prefetch
from django.db.models.query_utils import Q


class ODM2QuerySet(models.QuerySet):
    def for_display(self):
        return self.all()

    for_display.queryset_only = True


class AffiliationQuerySet(ODM2QuerySet):
    def for_display(self):
        return self.select_related('person').prefetch_related('organization')


class OrganizationQuerySet(ODM2QuerySet):
    def exclude_vendors(self):
        return self.exclude(organization_type__in=['Vendor', 'Manufacturer'])

    def only_vendors(self):
        return self.filter(organization_type__in=['Vendor', 'Manufacturer'])


class MethodQuerySet(ODM2QuerySet):
    def instrument_deployment_methods(self):
        return self.filter(method_type='Instrument deployment')

    def equipment_deployment_methods(self):
        return self.filter(method_type='Equipment deployment')

    def instrument_retrieval_methods(self):
        return self.filter(method_type='Instrument retrieval')

    def equipment_retrieval_methods(self):
        return self.filter(method_type='Equipment retrieval')

    def instrument_calibration_methods(self):
        return self.filter(method_type='Instrument calibration')

    def equipment_maintenance_methods(self):
        return self.filter(method_type='Equipment maintenance')

    def generic_action_methods(self):
        return self.exclude(method_type__in=[
            'Equipment deployment',
            'Instrument deployment',
            'Equipment maintenance',
            'Equipment retrieval',
            'Instrument retrieval',
            'Instrument calibration',
            'Field activity'
        ])


class ActionQuerySet(ODM2QuerySet):
    def deployments(self):
        return self.filter(action_type__in=['Equipment deployment', 'Instrument deployment'])

    def equipment_deployments(self):
        return self.filter(action_type='Equipment deployment')

    def instrument_deployments(self):
        return self.filter(action_type='Instrument deployment')

    def equipment_retrievals(self):
        return self.filter(action_type='Equipment retrieval')

    def instrument_retrievals(self):
        return self.filter(action_type='Instrument retrieval')

    def site_visits(self):
        return self.filter(action_type='Field activity')

    def instrument_calibrations(self):
        return self.filter(action_type='Instrument calibration')

    def equipment_maintenance(self):
        return self.filter(action_type='Equipment maintenance')

    def generic_actions(self):
        return self.exclude(action_type__in=[
            'Equipment deployment',
            'Instrument deployment',
            'Equipment maintenance',
            'Equipment retrieval',
            'Instrument retrieval',
            'Instrument calibration',
            'Field activity'
        ])

    def with_parent_visits(self):
        related_action_model = [
            related_object.related_model
            for related_object in self.model._meta.related_objects
            if related_object.name == 'related_actions'
        ].pop()

        return self.prefetch_related(Prefetch(
            lookup='related_actions',
            queryset=related_action_model.objects.filter(relationship_type_id='Is child of'),
            to_attr='all_parent_site_visits'))


class ActionTypeQuerySet(ODM2QuerySet):
    def generic_action_types(self):
        return self.exclude(name__in=['Equipment deployment', 'Instrument deployment', 'Instrument calibration', 'Site visit'])


class ActionByQuerySet(ODM2QuerySet):
    def for_display(self):
        return self.select_related('action').prefetch_related('affiliation__person', 'affiliation__organization')


class FeatureActionQuerySet(ODM2QuerySet):
    def for_display(self):
        return self.select_related('action').prefetch_related('sampling_feature')

    def with_results(self):
        return self.prefetch_related('results__timeseriesresult__values', 'results__variable', 'results__unit')


class RelatedActionQuerySet(ODM2QuerySet):
    def retrieval_relationships(self):
        return self.prefetch_related('related_action').filter(relationship_type='Is retrieval for')


class ResultManager(models.Manager):
    def get_queryset(self):
        queryset = super(ResultManager, self).get_queryset()
        return queryset.prefetch_related(
            'variable', 'unit', 'taxonomic_classifier', 'processing_level'
        )


class DataLoggerFileManager(models.Manager):
    def get_queryset(self):
        queryset = super(DataLoggerFileManager, self).get_queryset()
        return queryset.prefetch_related('program')


class DataLoggerFileColumnManager(models.Manager):
    def get_queryset(self):
        queryset = super(DataLoggerFileColumnManager, self).get_queryset()
        return queryset.DataLoggerFileColumnManager('result')

# endregion

# region ODM2 Equipment Extension


class EquipmentModelQuerySet(ODM2QuerySet):
    def for_display(self):
        return self.prefetch_related('model_manufacturer')


class EquipmentQuerySet(ODM2QuerySet):
    def instruments(self):
        return self.prefetch_related('equipment_model').filter(equipment_model__is_instrument=True)

    def non_instruments(self):
        return self.prefetch_related('equipment_model').filter(equipment_model__is_instrument=False)


class InstrumentOutputVariableManager(models.Manager):
    def get_queryset(self):
        queryset = super(InstrumentOutputVariableManager, self).get_queryset()
        return queryset.prefetch_related('model', 'variable', 'instrument_method', 'instrument_raw_output_unit')


class EquipmentManager(models.Manager):
    def get_queryset(self):
        queryset = super(EquipmentManager, self).get_queryset()
        return queryset.prefetch_related('equipment_model', 'equipment_owner', 'equipment_vendor')


class CalibrationReferenceEquipmentManager(models.Manager):
    def get_queryset(self):
        queryset = super(CalibrationReferenceEquipmentManager, self).get_queryset()
        return queryset.prefetch_related('action', 'equipment')


class EquipmentUsedManager(models.Manager):
    def get_queryset(self):
        queryset = super(EquipmentUsedManager, self).get_queryset()
        return queryset.prefetch_related('action', 'equipment')


class MaintenanceActionManager(models.Manager):
    def get_queryset(self):
        queryset = super(MaintenanceActionManager, self).get_queryset()
        return queryset.prefetch_related('action')


class RelatedEquipmentManager(models.Manager):
    def get_queryset(self):
        queryset = super(RelatedEquipmentManager, self).get_queryset()
        return queryset.prefetch_related('equipment', 'related_equipment')


class CalibrationActionManager(models.Manager):
    def get_queryset(self):
        queryset = super(CalibrationActionManager, self).get_queryset()
        return queryset.prefetch_related('instrument_output_variable')

# endregion


class TimeSeriesValuesQuerySet(ODM2QuerySet):
    def recent(self):
        return self.filter(value_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=1))
