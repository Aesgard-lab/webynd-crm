from django.urls import path, include
from rest_framework.routers import DefaultRouter
from staff.views.staff import StaffViewSet

from staff.views.salarios import StaffSalaryView  # <- asegúrate de que este archivo exista
from staff.views.salary_rules import SalaryRuleViewSet

router = DefaultRouter()
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'salary-rules', SalaryRuleViewSet, basename='salary-rules')


urlpatterns = [
    path('', include(router.urls)),
    path('staff/<int:staff_id>/salario/', StaffSalaryView.as_view(), name='staff-salary'),
]
