
from django.urls import path

from replacement.views import KfcListingView, StarbucksListingView, \
    BurgerkingListingView, PizzahutListingView, ReplacementCalculationView, HardwareUpdateView, HardwareCreateView, \
    HomePageTemplateView, HardwareDeleteView, HardwareDetailListingView

app_name = 'replacement'

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name='home-page'),
    path('kfc/', KfcListingView.as_view(), name='kfc-list'),
    path('sbx/', StarbucksListingView.as_view(), name='sbx-list'),
    path('bk/', BurgerkingListingView.as_view(), name='bk-list'),
    path('ph/', PizzahutListingView.as_view(), name='ph-list'),
    path('form/<int:pk>/', ReplacementCalculationView.as_view(), name='replacement-calculation'),
    path('hw-update/<int:pk>/', HardwareUpdateView.as_view(), name='hw-update'),
    path('hw-create/', HardwareCreateView.as_view(), name='hw-create'),
    path('hardware-delete/<int:pk>/', HardwareDeleteView.as_view(), name='hw-delete'),
    path('hw-detail/<int:pk>/', HardwareDetailListingView.as_view(), name='hw-detail'),
]

