#————————-urls employ—————-
from django.urls import path
from .views import (DesignationView,
                    DepartmentView,
                    EmployeeQualificationView,
                    EmployeeView,
                    QualificationView,
                    AvailableEmployeeListViewByScore,)
                    # EmployeeScoresView)

urlpatterns = [
 # Employee endpoints for listing and creating employees
    path('employees/', EmployeeView.as_view(), name='employee-list-create'),
    
    # Designation endpoint for listing all designations
    path('designations/', DesignationView.as_view(), name='designation-list'),

    # Department endpoint for listing all departments
    path('departments/', DepartmentView.as_view(), name='department-list'),

    # Qualification endpoints for listing and creating qualifications
    path('qualifications/', QualificationView.as_view(), name='qualification-list-create'),

    # EmployeeQualification endpoints for listing and creating employee qualifications
    path('employee-qualifications/', EmployeeQualificationView.as_view(), name='employee-qualification-list-create'),

    # path('filter-employee/', AvailableEmployeeListView.as_view(), name='filter-employee'),

    path('filter-employee/', AvailableEmployeeListViewByScore.as_view(), name='filter-employee')
]