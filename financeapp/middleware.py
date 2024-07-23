# middleware.py

from django.shortcuts import get_object_or_404
from .models import Budget
from django.shortcuts import render

class SelectedBudgetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        selected_budget_id = request.session.get('selected_budget_id')
        if selected_budget_id:
            request.selected_budget = get_object_or_404(Budget, id=selected_budget_id, user=request.user)
        else:
            request.selected_budget = None
        response = self.get_response(request)
        return response
