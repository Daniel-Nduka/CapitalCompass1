from .models import Budget

def selected_budget(request):
    return {
        'selected_budget': getattr(request, 'selected_budget', None)
    }