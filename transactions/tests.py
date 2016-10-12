# coding: utf-8

from django.contrib.auth.models import User
from django.test import TestCase, Client

from transactions.models import Account, Transaction


def set_up_user_accounts():
    ids = []
    nikola = User.objects.create_superuser(
        username='nikola',
        email='nikola@vts.rs',
        first_name='Nikola',
        last_name='Petrović',
        password='asdqwe123',
    )

    a = Account(owner=nikola, currency=Account.PHILIPPINE_PESO)
    a.save()
    ids.append(a.id)

    maja = User.objects.create_user(
        username='maja',
        email='maja@vts.rs',
        first_name='Maja',
        last_name='Marković',
        password='asdqwe123'
    )

    a = Account(owner=maja, currency=Account.PHILIPPINE_PESO)
    a.save()
    ids.append(a.id)

    return ids


def change_balance(account, balance):
    account.balance = balance
    account.save()


class AccountUnitTest(TestCase):

    def setUp(self):
        set_up_user_accounts()

    def test_account_balance(self):
        """"Assert defaults for _Account_.

        Defaults should be balance: 0 and currency: PHP
        """
        nikola = User.objects.get(username='nikola')
        nikolas_account = Account.objects.get(owner=nikola)
        self.assertEqual(nikolas_account.balance, 0)
        self.assertEqual(nikolas_account.currency, 'PHP')


class TransactionUnitTest(TestCase):

    def setUp(self):
        ids = set_up_user_accounts()
        self.account_1 = Account.objects.get(id=ids[0])
        self.account_2 = Account.objects.get(id=ids[1])
        change_balance(self.account_1, 100)
        change_balance(self.account_2, 100)

    def test_transaction(self):
        """Test a _Transaction_.

        Try to send an amount of 10 something and assert that balances are
        correct.
        """
        t = Transaction()
        t.start(self.account_1, self.account_2, 10)

        self.account_1.refresh_from_db()
        self.account_2.refresh_from_db()

        self.assertEqual(self.account_1.balance, 90)
        self.assertEqual(self.account_2.balance, 110)


class AccountApiTest(TestCase):

    def setUp(self):
        self.ids = set_up_user_accounts()

    def test_create(self):
        """Create an _Account_.

        Creation of an _Account_ with defaults should succeed and return a
        201 CREATED status code.
        """
        client = Client()
        client.force_login(User.objects.get(username='nikola'))
        response = client.post('/accounts/', {'owner': self.ids[0]})
        self.assertEqual(response.status_code, 201)


class TransactionApiTest(TestCase):

    def setUp(self):
        self.ids = set_up_user_accounts()
        self.account_1 = Account.objects.get(id=self.ids[0])
        self.account_2 = Account.objects.get(id=self.ids[1])

    def test_create_fail(self):
        """Fail to create a _Transaction_ because of lack of funds."""
        client = Client()
        client.force_login(User.objects.get(username='nikola'))
        response = client.post(
            '/payments/',
            {
                'from_account': self.ids[0],
                'to_account': self.ids[1],
                'amount': 100
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_create(self):
        """Succeed in creating a _Transaction_."""
        change_balance(self.account_1, 200)
        client = Client()
        client.force_login(User.objects.get(username='nikola'))
        response = client.post(
            '/payments/',
            {
                'from_account': self.ids[0],
                'to_account': self.ids[1],
                'amount': 100
            }
        )
        self.assertEqual(response.status_code, 201)
