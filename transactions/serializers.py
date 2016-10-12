
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    """Serialize :class:`transactions.models.Account`.

    Default :class:`serializers.ModelSerializer` behaviour is accepted.

    """

    class Meta:
        model = Account


class TransactionSerializer(serializers.ModelSerializer):
    """Serialize :class:`transactions.models.Transaction`.

    All fields from :class:`Transaction` are being shown, but there are three
    which are read-only, i.e. aren't accepted when POSTing data.

    """

    class Meta:
        model = Transaction
        fields = ('from_account', 'to_account', 'amount',
                  'id', 'created_ts', 'started_ts')
        read_only_fields = ('id', 'created_ts', 'started_ts')

    def create(self, validated_data):
        """Create a Transaction object from POST data.

        When creating a :class:`transactions.models.Transaction`, its
        :meth:`transactions.models.Transaction.start` method is being called,
        and the transaction is commited and the object saved.

        :param validated_data: Validated data gathered from the POST.
        :type validated_data: dict
        """
        transaction = Transaction()
        try:
            transaction.start(validated_data['from_account'],
                              validated_data['to_account'],
                              validated_data['amount'])
        except Exception as e:
            raise ValidationError(e.message)

        return transaction
