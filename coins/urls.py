
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from transactions.views import AccountViewSet, TransactionViewSet


router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'payments', TransactionViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
