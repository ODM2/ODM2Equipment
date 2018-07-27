from equipment_inventory.models import RetrievalRelatedAction
from odm2.models import Result, FeatureAction, MaintenanceAction, RelatedAction


def get_action_sampling_feature(action):
    feature_action = action.feature_actions.first()
    return feature_action and feature_action.sampling_feature


def pre_save_result(request, form, formset, formset_form, parent_site_visit, change):
    if not formset_form.instance.pk:
        formset_form.instance.result_type_id = 'Time series coverage'


def pre_save_feature_action(request, form, formset, formset_form, parent_site_visit, change):
    if 'parent_site_visit' in form.changed_data:
        formset_form.instance.sampling_feature = get_action_sampling_feature(parent_site_visit)
    elif not parent_site_visit:
        # site visit stand-alone
        pass


def pre_save_factory_service(request, form, formset, formset_form, parent_site_visit, change):
    if not formset_form.instance.pk:
        formset_form.instance.is_factory_service = True


def pre_save_related_deployment_action(request, form, formset, formset_form, parent_site_visit, change):
    if not formset_form.instance.pk:
        formset_form.instance.relationship_type_id = 'Is retrieval for'


class StandaloneActionAdminMixin(object):
    action_type = None
    formset_pre_save = {
        Result: pre_save_result,
        FeatureAction: pre_save_feature_action,
        MaintenanceAction: pre_save_factory_service,
        RetrievalRelatedAction: pre_save_related_deployment_action,
    }

    def save_parent_relationship(self, form, change, parent_site_visit):
        # save parent site visit as related action.
        if change and 'parent_site_visit' in form.changed_data:
            form.instance.related_actions.filter(relationship_type_id='Is child of').update(
                related_action=parent_site_visit)
        elif not change:
            form.instance.related_actions.create(relationship_type_id='Is child of', related_action=parent_site_visit)

    def save_model(self, request, obj, form, change):
        if not obj.action_type_id:
            obj.action_type_id = self.action_type
        obj.save()

    def save_related(self, request, form, formsets, change):
        parent_site_visit = None
        if 'parent_site_visit' in form.data:
            parent_site_visit = form.cleaned_data['parent_site_visit']
            self.save_parent_relationship(form, change, parent_site_visit)

        form.save_m2m()
        for formset in formsets:
            for formset_form in formset.forms:
                if formset.model in self.formset_pre_save:
                    self.formset_pre_save[formset.model](request, form, formset, formset_form, parent_site_visit, change)
            self.save_formset(request, form, formset, change=change)
