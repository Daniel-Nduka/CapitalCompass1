from django.contrib import admin
from .models import Budget, FiftyThirtyTwentyCategory, Expense, ZeroBasedCategory, Account, UserProfile, Transaction

admin.site.register(Budget)
admin.site.register(FiftyThirtyTwentyCategory)
admin.site.register(Expense)
admin.site.register(ZeroBasedCategory)
admin.site.register(Account)
admin.site.register(UserProfile)
admin.site.register(Transaction)
