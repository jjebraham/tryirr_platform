from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('market/', views.MarketListView.as_view(), name='market'),
    path('market/new/', views.OfferCreateView.as_view(), name='offer_create'),
    path('market/<int:offer_id>/trade/', views.place_trade, name='place_trade'),
    path('trades/', views.MyTradesListView.as_view(), name='trades'),
    path('trades/<int:pk>/', views.TradeDetailView.as_view(), name='trade_detail'),
    path('wallet/', views.WalletView.as_view(), name='wallet'),
]
