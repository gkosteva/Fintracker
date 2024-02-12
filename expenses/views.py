from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences
from datetime import datetime, date, timedelta


# Create your views here.
def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except Exception as identifier:
        currency = "Not set default currency"
        messages.info(request, "Please go to General Settings to set your currency")
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }

    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
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


@login_required(login_url='/authentication/login')
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


@login_required(login_url='/authentication/login')
def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense successfully removed!")
    return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_category_summary(request, month):
    def get_date(month_name):
        current_year = date.today().year
        month_date = datetime.strptime(month_name, '%B')
        month = month_date.month
        day = 1
        return date(current_year, month, day)

    def get_first_day_of_next_month(month_name):
        month_date = datetime.strptime(month_name, '%B')
        next_month_date = month_date + timedelta(days=31)
        next_month = next_month_date.month

        return next_month

    next_mont = get_first_day_of_next_month(month)
    if next_mont == 1:
        end_date = date(date.today().year + 1, next_mont, 1)
    else:
        end_date = date(date.today().year, next_mont, 1)
    month_date = get_date(month)
    expenses = Expense.objects.filter(owner=request.user, date__gte=month_date, date__lte=end_date)
    final_rep = {}

    def get_category(expense):
        return expense.category

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    category_list = list(set(map(get_category, expenses)))
    for x in expenses:
        for y in category_list:
            final_rep[y] = get_expense_category_amount(y)

    return JsonResponse({month: final_rep}, safe=False)


@login_required(login_url='/authentication/login')
def stats_view(request):
    return render(request, "expenses/stats.html")
