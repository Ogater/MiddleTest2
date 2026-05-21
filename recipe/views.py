from django.shortcuts import get_object_or_404, render

from .models import Category, Recipe


def main(request):
    """Display up to 10 random recipes, reshuffled on every page load."""
    recipes = Recipe.objects.order_by('?')[:10]
    return render(request, 'main.html', {'recipes': recipes})


def category_detail(request, category_id):
    """Display all recipes of a single category, looked up by its id."""
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'category_detail.html', {'category': category})
