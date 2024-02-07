from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences


# Create your views here.
@login_required(login_url='/authentication/login')
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = incomes.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    incomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user=request.user).currency
    context = {
        'incomes': incomes,
        'page_obj': page_obj,
        'currency': currency
    }

    return render(request, 'incomes/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == "GET":
        return render(request, 'incomes/add_income.html', context)
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["income_date"]
        source = request.POST["source"]
        if not amount:
            messages.error(request, "Amount should not be empty!")
            return render(request, 'incomes/add_income.html', context)

        Income.objects.create(owner=request.user, amount=amount, description=description, date=date, source=source)
        messages.success(request, "Income successfully created!")
        return redirect('incomes')


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == "GET":
        return render(request, 'incomes/income_edit.html', context)
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["income_date"]
        source = request.POST["source"]
        if not amount:
            messages.error(request, "Amount should not be empty!")
            return render(request, 'incomes/income_edit.html', context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.date = date
        income.source = source
        income.save()
        messages.success(request, "Income successfully updated!")
        return redirect('incomes')


@login_required(login_url='/authentication/login')
def income_delete(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income successfully removed!")
    return redirect('incomes')
