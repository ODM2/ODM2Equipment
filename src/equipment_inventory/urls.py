"""odm2sensor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import path

from equipment_inventory.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sites', SiteListView.as_view(), name='sites-list'),
    path('sites/<sampling_feature_code>', SiteDetailView.as_view(), name='site-detail'),
    path('results', ResultsListView.as_view(), name='results-list'),
    path('results/<result_id>', ResultDetailView.as_view(), name='result-detail'),
    path('site-visits', SiteVisitListView.as_view(), name='site-visit-list'),
    path('site-visits/<action_id>', SiteVisitDetailView.as_view(), name='site-visit-detail'),
    path('people', PeopleListView.as_view(), name='people-list'),
    path('people-detail/<person_id>', PeopleDetailView.as_view(), name='people_detail'),
    path('calibrations', CalibrationActionListView.as_view(), name='calibrations'),
    path('calibrations/<int:pk>', CalibrationActionDetailView.as_view(), name='calibration')
]
