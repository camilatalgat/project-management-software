from django.urls import path
from . import views

urlpatterns = [
    path('sprint/<int:sprint_id>/burndown/', views.burndown_chart_view, name='burndown-chart'),
    # path('api/sprint/<int:sprint_id>/burndown/', views.BurndownChartDataView.as_view(), name='burndown-data'),
    # path('sprint/<int:sprint_id>/burndown/', views.burndown_chart_view, name='burndown-chart'),
    # path('sprint/<int:sprint_id>/burndown', views.burndown_chart_view, name='burndown-chart'),  
    # path('api/sprint/<int:sprint_id>/burndown/', views.BurndownChartDataView.as_view(), name='burndown-data'),

]