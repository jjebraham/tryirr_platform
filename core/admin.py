from django.contrib import admin

from .models import Offer, Trade, Wallet, ChatMessage, WalletTransaction, CustomUser

admin.site.register(CustomUser)
admin.site.register(Offer)
admin.site.register(Trade)
admin.site.register(Wallet)
admin.site.register(ChatMessage)
admin.site.register(WalletTransaction)
