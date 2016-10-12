
from rest_framework import viewsets, mixins
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """A viewset that provides `create`, `list` and `retrieve` actions."""

    pass


class AccountViewSet(viewsets.ModelViewSet):
    """_Account_ handling.

    GET
    ---
    Returns all _Accounts_.

    POST
    ----
    Create new _Account_. Django _User_ has to be created in order to
    assign it to the Account being created.

        {
            "owner": 1,
            "balance": 100,
            "currency": "PHP"
        }

    Owner is the _User_ id.
    Various currencies are supported, but no conversions are implemented.
    PHP (Philippine Peso) is the default one.

    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(CreateListRetrieveViewSet):
    """_Transaction_ handling.

    Allowed operations are GET and POST. Accepts json data format.
    Transaction objects describe payments between _Accounts_.

    GET
    ---
    Returns all _Transaction_ objects.

    POST
    ----
    Accepts json data.

        {
            "from_account": 1,
            "to_account": 2,
            "amount": 100
        }

    This would start a transaction from account with id=1 to account id=2
    in the amount of 100. Currency isn't being checked, but should be.

    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
