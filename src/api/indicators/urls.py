from django.urls import path
from api.indicators import views
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import RedirectView

urlpatterns = [
    path('projetos/<pronac>', csrf_exempt(views.ProjectInfoView.as_view()),
         name='project_info_view'),
    url(r'^projetos', csrf_exempt(views.SearchProjectView.as_view()),
        name='search_project_view'),
    url(r'^docs', get_swagger_view(title='SalicML API'), name='swagger_index'),
    url(r'^', RedirectView.as_view(pattern_name='swagger_index', permanent=False)),
]
