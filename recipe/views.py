from django.shortcuts import render

from .models import Recipe


def main(request):
    """Display up to 10 random recipes, reshuffled on every page load."""
    recipes = Recipe.objects.order_by('?')[:10]
    return render(request, 'main.html', {'recipes': recipes})
