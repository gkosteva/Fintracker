from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add_expense', views.add_expense, name="add-expenses"),
    path('expense_edit/<int:id>', views.expense_edit, name="expense_edit"),
    path('expense_delete/<int:id>', views.expense_delete, name="expense_delete"),
    path('search-expenses', csrf_exempt(views.search_expense), name="search-expenses"),
    path('expense_category_summary/<str:month>', views.expense_category_summary, name="expense_category_summary"),
    path('stats_view', views.stats_view, name="stats_view")
]
