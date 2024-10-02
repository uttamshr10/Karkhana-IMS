from django.contrib import messages
from .forms import StandardInventoryCSVUploadForm, LocationCSVUploadForm
from django.shortcuts import render, redirect, get_object_or_404
from app import forms, models, filters
from django.db import transaction
import csv
from django.db.models import F, FloatField
from django.db.models.functions import Cast


def home(request):
    context = {}
    return render(request, 'app/home.html', context)

# def addUnit(request):
#     if request.method == 'POST':
#         form = forms.UnitForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/units')
#     else:
#         form = forms.UnitForm()
#     context ={
#         'form': form
#     }
#     return render(request, 'app/unit/createUnit.html', context)


# def showUnits(request):
#     units = models.Unit.objects.all()

#     starts_with = request.GET.get('starts_with_value')
#     if starts_with:
#         units = units.filter(name__istartswith=starts_with)

#     ends_with = request.GET.get('ends_with_value')
#     if ends_with:
#         units = units.filter(name__iendswith=ends_with)

#     search_query = request.GET.get('name')
#     if search_query:
#         units = units.filter(name__icontains=search_query)

#     context = {
#         'units': units,
#     }
#     return render(request, 'app/unit/units.html', context)

ADMIN_PASSWORD = "karkhana"


# def verify_unit(request):
#     if request.method == 'POST':
#         password = request.POST.get('password')
#         action_url = request.POST.get('action_url')

#         if password == ADMIN_PASSWORD:
#             return redirect(action_url)
#         else:
#             units = models.Unit.objects.all()
#             messages.error(request, "Your password is incorrect. Please reach out to your <a class='black' href='mailto:uttam@karkhana.asia' target='_blank'>admin</a>.")
#             return render(request, 'app/unit/units.html', {'units': units})
#     return redirect('/home')

def verify_inventory(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        action_url = request.POST.get('action_url')
        if password == ADMIN_PASSWORD:
            return redirect(action_url)
        else:
            inventories = models.Inventory.objects.all()
            for inventory in inventories:
                inventory.total_price = round(float(inventory.name.price_per_unit) * float(inventory.quantity))
            messages.error(request, "Your password is incorrect. Please reach out to your <a class='black' href='mailto:uttam@karkhana.asia' target='_blank'>admin</a>.")
            return render(request, 'app/inventory/inventories.html', {'inventories': inventories})
    return redirect('/home')

def verify_recipe(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        action_url = request.POST.get('action_url')

        if password == ADMIN_PASSWORD:
            return redirect(action_url)
        else:
            recipes = models.Recipe.objects.all()
            messages.error(request, "Your password is incorrect. Please reach out to your <a class='black' href='mailto:uttam@karkhana.asia' target='_blank'>admin</a>.")
            return render(request, 'app/recipe/recipes.html', {'recipes': recipes})
    return redirect('/home')

def verify_upload(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        action_url = request.POST.get('action_url')

        if password == ADMIN_PASSWORD:
            return redirect(action_url)
        else:
            messages.error(request, "Your password is incorrect. Please reach out to your <a class='black' href='mailto:uttam@karkhana.asia' target='_blank'>admin</a>.")
            return render(request, 'app/home.html', context={})

# def updateUnit(request, pk):
#     unit = get_object_or_404(models.Unit, pk=pk)
#     if request.method == 'POST':
#         form = forms.UnitForm(request.POST, instance = unit)
#         if form.is_valid():
#             form.save()
#             return redirect('/units')
#     else:
#         form = forms.UnitForm(instance = unit)
#     context = {
#         'form': form,
#         'unit': unit
#     }
#     return render(request, 'app/unit/updateUnit.html', context)

# def deleteUnit(request, pk):
#     unit = get_object_or_404(models.Unit, pk=pk)
#     if request.method == 'POST':
#         unit.delete()
#         return redirect('/units')
#     context = {
#         'unit': unit
#     }
#     return render(request, 'app/unit/deleteUnit.html', context)

def addInventory(request):
    if request.method == 'POST':
        form = forms.InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/inventories')
    else:
        form = forms.InventoryForm()
    context = {
        'form': form
    }
    return render(request, 'app/inventory/createInventory.html', context)


def showInventories(request):
    inventories = models.Inventory.objects.all()
    standard = models.StandardInventory.objects.all()

    inventories = inventories.annotate(
        total_price=Cast(F('name__price_per_unit') * F('quantity'), FloatField())
    )

    starts_with = request.GET.get('starts_with_value')
    if starts_with:
        inventories = inventories.filter(name__name__istartswith=starts_with)

    ends_with = request.GET.get('ends_with_value')
    if ends_with:
        inventories = inventories.filter(name__name__iendswith=ends_with)

    search_query = request.GET.get('name')
    if search_query:
        inventories = inventories.filter(name__name__icontains=search_query)

    find_query = request.GET.get('find')
    if find_query:
        inventories = inventories.filter(location__name__icontains=find_query)

    quantity_range = request.GET.get('quantity_range')
    if quantity_range:
        if quantity_range == "0-1000":
            inventories = inventories.filter(quantity__gte=0, quantity__lte=1000)
        elif quantity_range == "1001-5000":
            inventories = inventories.filter(quantity__gte=1001, quantity__lte=5000)
        elif quantity_range == "5001-10000":
            inventories = inventories.filter(quantity__gte=5001, quantity__lte=10000)
        elif quantity_range == "10000+":
            inventories = inventories.filter(quantity__gte=10000)
    
    price_range = request.GET.get('price_range')
    if price_range:
        if price_range == "0-5000":
            inventories = inventories.filter(total_price__gte=0, total_price__lte=5000)
        elif price_range == "5001-10000":
            inventories = inventories.filter(total_price__gte=5001, total_price__lte=10000)
        elif price_range == "10000+":
            inventories = inventories.filter(total_price__gte=10000)


    for inventory in inventories:
        inventory.total_price = round(float(inventory.name.price_per_unit) * float(inventory.quantity))

    context = {
        'inventories': inventories,
        'standard': standard,
    }
    return render(request, 'app/inventory/inventories.html', context)

def updateInventory(request, pk):
    inventory = get_object_or_404(models.Inventory, pk=pk)
    if request.method == 'POST':
        form = forms.InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('/inventories')
    else:
        form = forms.InventoryForm(instance = inventory)
    context = {
        'form': form,
        'inventory': inventory
    }
    return render(request, 'app/inventory/updateInventory.html', context)

def deleteInventory(request, pk):
    inventory = get_object_or_404(models.Inventory, pk=pk)
    if request.method == 'POST':
        inventory.delete()
        return redirect('/inventories')
    context = {
        'inventory': inventory
    }
    return render(request, 'app/inventory/deleteInventory.html', context)

# for creating new recipe name:
# def addRecipe(request):
#     if request.method == 'POST':
#         form = forms.RecipeForm(request.POST)
#         dropdown = forms.RecipeItemForm(request.POST)
#         if form.is_valid() and dropdown.is_valid():
#             form.save()
#             return redirect('/recipes')
#     else:
#         form = forms.RecipeForm()
#         dropdown = forms.RecipeItemForm()
#     context = {
#         'form': form,
#         'dropdown': dropdown
#     }
#     return render(request, 'app/recipe/createRecipe.html', context)


def addRecipe(request):
    if request.method == 'POST':
        form = forms.RecipeForm(request.POST)
        dropdown = forms.RecipeItemForm(request.POST)
        if form.is_valid() and dropdown.is_valid():
            recipe = form.save()
            recipe_item = dropdown.save(commit=False)
            recipe_item.recipe = recipe
            recipe_item.save()
            return redirect('/recipes')
    else:
        form = forms.RecipeForm()
        dropdown = forms.RecipeItemForm()
    
    context = {
        'form': form,
        'dropdown': dropdown
    }
    return render(request, 'app/recipe/createRecipe.html', context)


def showRecipes(request):
    recipes = models.Recipe.objects.all()
    
    starts_with = request.GET.get('starts_with_value')
    if starts_with:
        recipes = recipes.filter(name__istartswith=starts_with)

    ends_with = request.GET.get('ends_with_value')
    if ends_with:
        recipes = recipes.filter(name__iendswith=ends_with)

    search_query = request.GET.get('name')
    if search_query:
        recipes = recipes.filter(name__icontains=search_query)

    for recipe in recipes:
        total_unit_price = 0
        total_quantity = 0
        items = recipe.items.all()  # Get all RecipeItems related to the recipe

        # Calculate total price and total quantity for the recipe
        for item in items:
            total_unit_price += item.inventory.name.price_per_unit * item.quantity  # Total price for the item
            total_quantity += item.quantity  # Add to total quantity

        # Attach totals to the recipe object
        recipe.total_unit_price = total_unit_price
        recipe.total_quantity = total_quantity
    context = {
        'recipes': recipes,
    }
    return render(request, 'app/recipe/recipes.html', context)

# for updating recipe name:
# def updateRecipe(request, pk):
#     recipe = get_object_or_404(models.RecipeItem, pk=pk)
#     if request.method == 'POST':
#         form = forms.RecipeItemForm(request.POST, instance = recipe)
#         if form.is_valid():
#             recipe.save()
#             return redirect('/recipes')
#     else:
#         form = forms.RecipeItemForm(instance = recipe)
#     context ={
#         'form': form
#     }
#     return render(request, 'app/recipe/updateRecipe.html', context)


def deleteRecipe(request, pk):
    recipe = get_object_or_404(models.Recipe, pk = pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('/recipes')
    context = {
        'recipe': recipe
    }
    return render(request, 'app/recipe/deleteRecipe.html', context)


# create
def createRecipe(request):
    if request.method == 'POST':
        recipe_form = forms.RecipeForm(request.POST)
        if recipe_form.is_valid():
            recipe = recipe_form.save()
            formset = forms.RecipeItemFormSetForCreate(request.POST, instance = recipe)
            if formset.is_valid():
                formset.save()
                return redirect('/recipes')
    else:
        recipe_form = forms.RecipeForm()
        formset = forms.RecipeItemFormSetForCreate()

    context = {
        'recipe_form': recipe_form,
        'formset': formset
    }
    return render(request, 'app/recipe/createRecipe.html', context)


def editRecipe(request, pk):
    recipe = get_object_or_404(models.Recipe, id=pk)

    if request.method == 'POST':
        recipe_form = forms.RecipeForm(request.POST, instance=recipe)
        formset = forms.RecipeItemFormSetForEdit(request.POST, instance=recipe)

        if recipe_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                recipe_form.save()
                instances = formset.save(commit=False)
                                
                formset_ids = [form.instance.id for form in formset.forms if form.instance.id]
                
                # Delete items that are no longer in the formset
                recipe.items.exclude(id__in=formset_ids).delete()
                
                # Save or update the items in the formset
                for instance in instances:
                    instance.recipe = recipe
                    instance.save()
            return redirect('/recipes')
    else:
        recipe_form = forms.RecipeForm(instance=recipe)
        formset = forms.RecipeItemFormSetForEdit(instance=recipe)

    context = {
        'recipe_form': recipe_form,
        'formset': formset,
        'recipe': recipe
    }
    return render(request, 'app/recipe/updateRecipe.html', context)

# for csv only


def upload_inventory(request):
    if request.method == 'POST':
        form = StandardInventoryCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                code = row['code']
                inventory_name = row['name']
                unit_price = row['price_per_unit']

                models.StandardInventory.objects.create(
                    code = code,
                    name=inventory_name,
                    price_per_unit = unit_price,
                )

            messages.success(request, "CSV file has been uploaded successfully.")
            return redirect('/home')
    else:
        form = StandardInventoryCSVUploadForm()
    context = {
        'form': form
    }

    return render(request, 'app/inventory/inventory_upload.html', context)

def upload_location(request):
    if request.method == 'POST':
        form = LocationCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                name = row['location']

                models.Location.objects.create(
                    name = name
                )

            messages.success(request, "CSV file has been uploaded successfully.")
            return redirect('/home')
    else:
        form = LocationCSVUploadForm()
    context = {
        'form': form
    }

    return render(request, 'app/location/location_upload.html', context)


# def upload_unit(request):
#     if request.method == 'POST':
#         form = UnitCSVUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = request.FILES['csv_file']
#             decoded_file = csv_file.read().decode('utf-8').splitlines()
#             reader = csv.DictReader(decoded_file)

#             # Track names that have been processed to avoid duplicates
#             processed_names = set()

#             for row in reader:
#                 unit_name = row['unit']

#                 if unit_name in processed_names:
#                     continue  # Skip duplicate unit names
#                 processed_names.add(unit_name)

#                 if not unit_name:
#                     continue  # Skip empty unit names

#                 # Check if the unit already exists
#                 if models.Unit.objects.filter(name=unit_name).exists():
#                     messages.warning(request, f"Unit '{unit_name}' already exists.")
#                     continue

#                 # Create the new unit
#                 try:
#                     models.Unit.objects.create(name=unit_name)
#                 except Exception as e:
#                     messages.error(request, f"An error occurred while adding unit '{unit_name}': {e}")
#                     continue

#             messages.success(request, "CSV file has been uploaded successfully.")
#             return redirect('/home')
#     else:
#         form = UnitCSVUploadForm()
    
#     context = {
#         'form': form
#     }

#     return render(request, 'app/unit/unit_upload.html', context)

# def upload_recipe(request):
    
#     return render(request, 'app/recipe/recipe_upload.html')


# def create_recipes(request):
#     if request.method == 'POST':
#         form = forms.RecipeCreationForm(request.POST)
#         if form.is_valid():
#             recipes = form.cleaned_data['recipes']  # This is a list of selected recipes
#             quantity = form.cleaned_data['quantity']

#             required_ingredients = {}

#             # Loop over selected recipes and calculate required quantities
#             for recipe in recipes:
#                 recipe_items = models.RecipeItem.objects.filter(recipe=recipe)

#                 for item in recipe_items:
#                     required_quantity = item.quantity * quantity

#                     # Sum quantities if the same ingredient is used in multiple recipes
#                     if item.inventory.name in required_ingredients:
#                         required_ingredients[item.inventory.name] += required_quantity
#                     else:
#                         required_ingredients[item.inventory.name] = required_quantity

#             # Check inventory availability
#             out_of_stock = {}
#             for inv_name, req_quantity in required_ingredients.items():
#                 inventory = models.Inventory.objects.get(name=inv_name)
#                 if inventory.quantity < req_quantity:
#                     out_of_stock[inv_name] = {'needed': req_quantity, 'available': inventory.quantity}

#             if out_of_stock:
#                 # Redirect to the out_of_stock.html template
#                 return render(request, 'app/available/out_of_stock.html', {
#                     'out_of_stock': [{'item': k, 'needed': v['needed'], 'available': v['available']} for k, v in out_of_stock.items()]
#                 })
#             else:
#                 # Redirect to the confirm.html template with all selected recipes
#                 context = {
#                     'recipes': recipes,
#                     'number_of_recipes': quantity
#                 }
#                 return render(request, 'app/available/confirm.html', context)
#     else:
#         form = forms.RecipeCreationForm()

#     context = {
#         'form': form
#     }
#     return render(request, 'app/available/check.html', context)

from django.db.models import Sum

def create_recipes(request):
    if request.method == 'POST':
        form = forms.RecipeCreationForm(request.POST)
        if form.is_valid():
            recipes = form.cleaned_data['recipes']
            quantity = form.cleaned_data['quantity']

            required_ingredients = {}

            for recipe in recipes:
                recipe_items = models.RecipeItem.objects.filter(recipe=recipe)

                for item in recipe_items:
                    required_quantity = item.quantity * quantity
                    standard_inventory_id = item.inventory.name.id

                    if standard_inventory_id in required_ingredients:
                        required_ingredients[standard_inventory_id] += required_quantity
                    else:
                        required_ingredients[standard_inventory_id] = required_quantity

            out_of_stock = {}
            for standard_inv_id, req_quantity in required_ingredients.items():
                standard_inventory = models.StandardInventory.objects.get(id=standard_inv_id)
                total_quantity = models.Inventory.objects.filter(name=standard_inventory).aggregate(Sum('quantity'))['quantity__sum'] or 0

                if total_quantity < req_quantity:
                    remaining = req_quantity - total_quantity
                    out_of_stock[standard_inventory.name] = {'remaining': remaining}

            if out_of_stock:
                return render(request, 'app/available/out_of_stock.html', {
                    'out_of_stock': [{'item': k, 'remaining': v['remaining']} for k, v in out_of_stock.items()]
                })
            else:
                context = {
                    'recipes': recipes,
                    'number_of_recipes': quantity
                }
                return render(request, 'app/available/confirm.html', context)
    else:
        form = forms.RecipeCreationForm()

    context = {
        'form': form
    }
    return render(request, 'app/available/check.html', context)


def confirm_creation(request):
    if request.method == 'POST':
        recipe_ids = request.POST.getlist('recipes')
        number_of_recipes = int(request.POST.get('number_of_recipes'))
        confirm = request.POST.get('confirm')

        created_recipes = {}

        if confirm == 'yes':
            required_ingredients = {}

            for recipe_id in recipe_ids:
                recipe = models.Recipe.objects.get(id=recipe_id)
                recipe_items = models.RecipeItem.objects.filter(recipe=recipe)

                created_recipes[recipe] = number_of_recipes

                for item in recipe_items:
                    required_quantity = item.quantity * number_of_recipes
                    standard_inventory_id = item.inventory.name.id

                    if standard_inventory_id in required_ingredients:
                        required_ingredients[standard_inventory_id] += required_quantity
                    else:
                        required_ingredients[standard_inventory_id] = required_quantity

            out_of_stock = {}

            for standard_inv_id, req_quantity in required_ingredients.items():
                standard_inventory = models.StandardInventory.objects.get(id=standard_inv_id)
                total_quantity = models.Inventory.objects.filter(name=standard_inventory).aggregate(Sum('quantity'))['quantity__sum'] or 0

                if total_quantity < req_quantity:
                    out_of_stock[standard_inventory.name] = {'needed': req_quantity, 'available': total_quantity}

            if out_of_stock:
                return render(request, 'app/available/out_of_stock.html', {
                    'out_of_stock': [{'item': k, 'needed': v['needed'], 'available': v['available']} for k, v in out_of_stock.items()]
                })

            with transaction.atomic():
                for standard_inv_id, req_quantity in required_ingredients.items():
                    standard_inventory = models.StandardInventory.objects.get(id=standard_inv_id)
                    inventories = models.Inventory.objects.filter(name=standard_inventory).order_by('quantity')
                    
                    for inventory in inventories:
                        if req_quantity <= 0:
                            break
                        if inventory.quantity >= req_quantity:
                            inventory.quantity -= req_quantity
                            inventory.save()
                            break
                        else:
                            req_quantity -= inventory.quantity
                            inventory.quantity = 0
                            inventory.save()

            messages.success(request, f"Successfully created {number_of_recipes} recipes.")
            return render(request, 'app/available/success.html', {
                'created_recipes': created_recipes
            })
        else:
            messages.info(request, "Recipe creation cancelled.")
            return redirect('/recipes')

    return redirect('/recipes')


# def create_recipes(request):
#     if request.method == 'POST':
#         form = forms.RecipeCreationForm(request.POST)
#         if form.is_valid():
#             recipes = form.cleaned_data['recipes']  # This is a list of selected recipes
#             quantity = form.cleaned_data['quantity']

#             required_ingredients = {}

#             # Loop over selected recipes and calculate required quantities
#             for recipe in recipes:
#                 recipe_items = models.RecipeItem.objects.filter(recipe=recipe)

#                 for item in recipe_items:
#                     required_quantity = item.quantity * quantity

#                     # Sum quantities if the same ingredient is used in multiple recipes
#                     if item.inventory.name in required_ingredients:
#                         required_ingredients[item.inventory.name] += required_quantity
#                     else:
#                         required_ingredients[item.inventory.name] = required_quantity

#             # Check inventory availability and calculate remaining units needed
#             out_of_stock = {}
#             for inv_name, req_quantity in required_ingredients.items():
#                 inventory = models.Inventory.objects.get(name=inv_name)
#                 if inventory.quantity < req_quantity:
#                     remaining = req_quantity - inventory.quantity  # Calculate remaining units
#                     out_of_stock[inv_name] = {'remaining': remaining}

#             if out_of_stock:
#                 # Redirect to the out_of_stock.html template
#                 return render(request, 'app/available/out_of_stock.html', {
#                     'out_of_stock': [{'item': k, 'remaining': v['remaining']} for k, v in out_of_stock.items()]
#                 })
#             else:
#                 # Redirect to the confirm.html template with all selected recipes
#                 context = {
#                     'recipes': recipes,
#                     'number_of_recipes': quantity
#                 }
#                 return render(request, 'app/available/confirm.html', context)
#     else:
#         form = forms.RecipeCreationForm()

#     context = {
#         'form': form
#     }
#     return render(request, 'app/available/check.html', context)


# def confirm_creation(request):
#     if request.method == 'POST':
#         recipe_ids = request.POST.getlist('recipes')
#         number_of_recipes = int(request.POST.get('number_of_recipes'))
#         confirm = request.POST.get('confirm')

#         created_recipes = {}

#         if confirm == 'yes':
#             required_ingredients = {}

#             # Calculate required ingredients for all selected recipes
#             for recipe_id in recipe_ids:
#                 recipe = models.Recipe.objects.get(id=recipe_id)
#                 recipe_items = models.RecipeItem.objects.filter(recipe=recipe)

#                 created_recipes[recipe] = number_of_recipes  # Store the recipe and number of recipes created

#                 for item in recipe_items:
#                     required_quantity = item.quantity * number_of_recipes
#                     inventory = models.Inventory.objects.get(name=item.inventory.name)

#                     # Sum required quantities for each inventory item
#                     if inventory.name in required_ingredients:
#                         required_ingredients[inventory.name] += required_quantity
#                     else:
#                         required_ingredients[inventory.name] = required_quantity

#             out_of_stock = {}

#             # Check availability
#             for inv_name, req_quantity in required_ingredients.items():
#                 inventory = models.Inventory.objects.get(name=inv_name)
#                 if inventory.quantity < req_quantity:
#                     out_of_stock[inv_name] = {'needed': req_quantity, 'available': inventory.quantity}

#             if out_of_stock:
#                 return render(request, 'app/available/out_of_stock.html', {
#                     'out_of_stock': [{'item': k, 'needed': v['needed'], 'available': v['available']} for k, v in out_of_stock.items()]
#                 })

#             # Proceed with deduction
#             with transaction.atomic():
#                 for inventory_name, req_quantity in required_ingredients.items():
#                     inventory = models.Inventory.objects.select_for_update().get(name=inventory_name)
#                     inventory.quantity -= req_quantity
#                     inventory.save()

#             # Pass created recipes to the success page
#             messages.success(request, f"Successfully created {number_of_recipes} recipes.")
#             return render(request, 'app/available/success.html', {
#                 'created_recipes': created_recipes  # Pass the dictionary of created recipes and quantities
#             })
#         else:
#             messages.info(request, "Recipe creation cancelled.")
#             return redirect('/recipes')

#     return redirect('/recipes')

