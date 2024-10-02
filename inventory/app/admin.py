from django.contrib import admin
from app.models import Inventory, Recipe, RecipeItem, StandardInventory, Location

admin.site.register([Inventory, Recipe, RecipeItem, StandardInventory, Location])