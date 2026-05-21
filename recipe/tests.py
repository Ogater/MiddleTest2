from django.test import TestCase
from django.urls import reverse

from .models import Category, Recipe


def create_recipe(category, title='Recipe'):
    """Helper that builds a Recipe attached to the given category."""
    return Recipe.objects.create(
        title=title,
        description='Some description',
        instructions='Some instructions',
        ingredients='Some ingredients',
        category=category,
    )


class MainViewTests(TestCase):
    """Tests for the `main` view rendering main.html."""

    def setUp(self):
        self.category = Category.objects.create(name='Breakfast')
        self.url = reverse('main')

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_main_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'main.html')

    def test_context_contains_recipes(self):
        response = self.client.get(self.url)
        self.assertIn('recipes', response.context)

    def test_returns_at_most_10_recipes(self):
        for i in range(15):
            create_recipe(self.category, title=f'Recipe {i}')
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['recipes']), 10)

    def test_returns_all_recipes_when_fewer_than_10(self):
        for i in range(4):
            create_recipe(self.category, title=f'Recipe {i}')
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['recipes']), 4)

    def test_returns_empty_when_no_recipes(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['recipes']), 0)
        self.assertContains(response, 'No recipes found.')


class CategoryDetailViewTests(TestCase):
    """Tests for the `category_detail` view rendering category_detail.html."""

    def setUp(self):
        self.category = Category.objects.create(name='Soups')
        self.other_category = Category.objects.create(name='Desserts')
        self.recipe_a = create_recipe(self.category, title='Borscht')
        self.recipe_b = create_recipe(self.category, title='Ramen')
        self.other_recipe = create_recipe(self.other_category, title='Cheesecake')
        self.url = reverse('category_detail', args=[self.category.id])

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_category_detail_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'category_detail.html')

    def test_context_contains_requested_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['category'], self.category)

    def test_shows_only_recipes_of_the_category(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Borscht')
        self.assertContains(response, 'Ramen')
        self.assertNotContains(response, 'Cheesecake')

    def test_returns_404_for_unknown_category(self):
        unknown_url = reverse('category_detail', args=[9999])
        response = self.client.get(unknown_url)
        self.assertEqual(response.status_code, 404)

    def test_empty_category_renders_placeholder(self):
        empty_category = Category.objects.create(name='Empty')
        response = self.client.get(reverse('category_detail', args=[empty_category.id]))
        self.assertContains(response, 'No recipes found.')
