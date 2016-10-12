
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone


class Account(models.Model):
    """Class representing user Account.

    It is related to an User by a foreign key. It keeps track of account's
    balance and its currency.

    .. note::
        Accessing balance directly, or even via subtract and add methods
        isn't thread safe. You need to employ a strategy that would keep
        a lock over the rows or fields that need to be changed. You can find
        an example of such locking in the :class:`Transaction` class.

    """

    PHILIPPINE_PESO = 'PHP'
    US_DOLLAR = 'USD'
    EURO = 'EUR'
    SERBIAN_DINAR = 'RSD'
    CURRENCY_CHOICES = (
        (PHILIPPINE_PESO, 'Philippine Peso'),
        (US_DOLLAR, 'US Dollar'),
        (EURO, 'Euro'),
        (SERBIAN_DINAR, 'Serbian Dinar')
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default=PHILIPPINE_PESO)

    class Meta:
        app_label = 'transactions'

    def subtract_balance(self, amount):
        """Subtract balance from account.

        Subtract an amount from user's balance, if balance
        is higher than the amount needed.

        :param amount: The amount to subtract.
        :type amount: float
        :returns: bool -- True if subtraction has succeeded, False if not.

        """
        if self.balance < amount:
            result = False
        else:
            self.balance = self.balance - amount
            result = True
            self.save()

        return result

    def add_balance(self, amount):
        """Add an amount to account's balance.

        :param amount: The amount to add.
        :type amount: float
        :returns: True if the addition went good.

        """
        self.balance = self.balance + amount
        self.save()
        return True

    def __unicode__(self):
        """Return string representation of the Account.

        Returns a representation of the account in following format:
        1/nikola/100 (id/username/balance)

        :returns: str -- Account representation

        """
        return '%s/%s/%s' % (self.id, self.owner.username, self.balance)


class Transaction(models.Model):
    """Class representing a single transaction between two accounts.

    It has a notion of preserving atomicity in dealing with account balance
    by locking database on row level. Started timestamp is created when the
    transaction is started by using :meth:`start` method.

    """

    created_ts = models.DateTimeField(auto_now_add=True)
    started_ts = models.DateTimeField(null=True)
    from_account = models.ForeignKey(
        Account, related_name='from_account', on_delete=models.CASCADE)
    to_account = models.ForeignKey(
        Account, related_name='to_account', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        app_label = 'transactions'

    @transaction.atomic
    def start(self, from_account, to_account, amount):
        """Start a transaction between two accounts.

        .. note:
            This function minds the atomicity of the transaction.

        :param from_account: Account sending the payment.
        :type from_account: :class:`Account`
        :param to_account: Account receiving the payment.
        :type to_account: :class:`Account`
        :param amount: The amount which is being sent.
        :type amount: float

        """
        self.started_ts = timezone.now()
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

        if self.from_account.subtract_balance(amount):
            self.to_account.add_balance(amount)
        else:
            raise Exception('Not enough funds in %s' % self.from_account)

        self.save()
