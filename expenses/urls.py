from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add_expense', views.add_expense, name="add-expenses"),
    path('expense_edit/<int:id>', views.expense_edit, name="expense_edit"),
    path('expense_delete/<int:id>', views.expense_delete, name="expense_delete")
]
