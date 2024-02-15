from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="incomes"),
    path('add_income', views.add_income, name="add-incomes"),
    path('income_edit/<int:id>', views.income_edit, name="income_edit"),
    path('income_delete/<int:id>', views.income_delete, name="income_delete"),
    path('search-income', csrf_exempt(views.search_income), name="search_income"),
    path('income_category_summary/<str:month>', views.income_category_summary, name="income_category_summary"),
    path('stats_view', views.stats_view, name="stats_incomes_view")
]
