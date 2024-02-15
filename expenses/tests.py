from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Expense, Category

class TestExpenseViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.expense = Expense.objects.create(owner=self.user, amount=100, description='Test Expense', date=timezone.now(), category=self.category)

    def test_index_view(self):
        response = self.client.get(reverse('expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/index.html')
        self.assertContains(response, 'Test Expense')

    def test_add_expense_view(self):
        response = self.client.get(reverse('add-expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/add_expense.html')

        response = self.client.post(reverse('add-expenses'), {'amount': 200, 'description': 'New Expense', 'expense_date': "2024-02-15", 'category': self.category.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 2)

    def test_edit_expense_view(self):
        response = self.client.get(reverse('expense_edit', args=[self.expense.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/expense_edit.html')

        response = self.client.post(reverse('expense_edit', args=[self.expense.id]), {'amount': 150, 'description': 'Updated Expense', 'expense_date': "2024-02-15", 'category': self.category.id})
        self.assertEqual(response.status_code, 302)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.amount, 150)

    def test_delete_expense_view(self):
        response = self.client.post(reverse('expense_delete', args=[self.expense.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())

    # def test_search_expense_view(self):
    #     response = self.client.post(reverse('search-expenses'), {'searchText': 'Test'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(response.json()), 1)
    #     self.assertEqual(response.json()[0]['description'], 'Test Expense')
    #
    def test_expense_category_summary_view(self):
        month = timezone.now().strftime('%B')
        response = self.client.get(reverse('expense_category_summary', args=[month]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(list(response.json().keys())[0], month)

    def test_stats_view(self):
        response = self.client.get(reverse('stats_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/stats.html')
