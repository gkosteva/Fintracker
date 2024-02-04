from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense
from django.contrib import messages


# Create your views here.

@login_required(login_url='/authentication/login')
@never_cache
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    context = {
        'expenses': expenses
    }

    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == "GET":
        return render(request, 'expenses/add_expense.html', context)
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        if not amount:
            messages.error(request, "Amount should not be empty!")
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, description=description, date=date, category=category)
        messages.success(request, "Expense successfully created!")
        return redirect('expenses')


def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == "GET":
        return render(request, 'expenses/expense_edit.html', context)
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        if not amount:
            messages.error(request, "Amount should not be empty!")
            return render(request, 'expenses/expense_edit.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category
        expense.save()
        messages.success(request, "Expense successfully updated!")
        return redirect('expenses')


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense successfully removed!")
    return redirect('expenses')
