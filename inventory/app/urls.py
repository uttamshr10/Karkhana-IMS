from django.urls import path
from app import views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    # path('createUnit/', views.addUnit, name='addUnit'),
    # path('units/', views.showUnits, name='units'),
    # path('unit/update/<int:pk>/', views.updateUnit, name='updateUnit'),
    # path('unit/delete/<int:pk>/', views.deleteUnit, name='deleteUnit'),
    path('createInventory/', views.addInventory, name='addInventory'),
    path('inventories/', views.showInventories, name='inventories'),
    path('inventory/update/<int:pk>/', views.updateInventory, name='update'),
    path('inventory/delete/<int:pk>/', views.deleteInventory, name='delete'),
    path('createRecipe/', views.createRecipe, name='addRecipe'),
    path('recipes/', views.showRecipes, name='recipes'),
    path('recipe/edit/<int:pk>/', views.editRecipe, name='updateRecipe'),
    path('recipe/delete/<int:pk>/', views.deleteRecipe, name='deleteRecipe'),
    # for csv only
    path('upload_inventory/', views.upload_inventory, name="upload_inventory"),
    path('upload_location/', views.upload_location, name="upload_location"),
    # path('upload_unit/', views.upload_unit, name="upload_unit"),
    # path('upload_recipe/', views.upload_recipe, name='upload_recipe'),

    # for checking availability
    path('create-recipes/', views.create_recipes, name='create_recipes'),
    path('confirm/', views.confirm_creation, name='confirm_creation'),

    #password verification
    # path('verify-unit/', views.verify_unit, name='verify_unit'),
    path('verify-inventory/', views.verify_inventory, name='verify_inventory'),
    path('verify-recipe/', views.verify_recipe, name='verify_recipe'),
    path('verify-upload/', views.verify_upload, name='verify_upload'),
]