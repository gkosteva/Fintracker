from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Source, Income


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.source = Source.objects.create(name='Test Source')
        self.income = Income.objects.create(
            owner=self.user, amount=100, description='Test Income', source=self.source)

    # def test_search_income(self):
    #     response = self.client.post(reverse('search_income'), {'searchText': 'Test'})
    #     self.assertEqual(response.status_code, 200)

    # def test_index(self):
    #     response = self.client.get(reverse('incomes'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'incomes/index.html')

    def test_add_income_GET(self):
        response = self.client.get(reverse('add-incomes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/add_income.html')

    def test_add_income_POST(self):
        response = self.client.post(reverse('add-incomes'), {
            'amount': 200,
            'description': 'New Test Income',
            'income_date': '2024-02-15',
            'source': self.source.id
        })
        self.assertEqual(response.status_code, 302)

    def test_income_edit_GET(self):
        response = self.client.get(reverse('income_edit', args=[self.income.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/income_edit.html')

    def test_income_edit_POST(self):
        response = self.client.post(reverse('income_edit', args=[self.income.id]), {
            'amount': 150,
            'description': 'Updated Test Income',
            'income_date': '2024-02-16',
            'source': self.source.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful POST

    def test_income_delete(self):
        response = self.client.post(reverse('income_delete', args=[self.income.id]))
        self.assertEqual(response.status_code, 302)

    def test_income_category_summary(self):
        response = self.client.get(reverse('income_category_summary', args=['February']))
        self.assertEqual(response.status_code, 200)

    def test_stats_view(self):
        response = self.client.get(reverse('stats_incomes_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incomes/stats.html')
