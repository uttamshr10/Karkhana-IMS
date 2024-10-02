from django.db import models

class StandardInventory(models.Model):
    code = models.CharField(max_length = 15, default='')
    name = models.CharField(max_length=100)
    price_per_unit = models.FloatField(null = False, default = '')

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length = 50, null=False, default = '')

    def __str__(self):
        return self.name
        

class Inventory(models.Model):
    name = models.ForeignKey(StandardInventory, on_delete=models.CASCADE, related_name = 'inventory_names')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete = models.CASCADE, default = '')

    def __str__(self):
        return f'{str(self.name)} - {self.quantity}'
    

    

class Recipe(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    
class RecipeItem(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name = 'items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Recipe: {self.recipe} "

    def get_total_price(self):
        # Access the StandardInventory through the Inventory model
        price_per_unit = self.inventory.name.price_per_unit
        total_price = price_per_unit * self.quantity
        return total_price
    
    def price_per_unit(self):
        price_per_unit = self.inventory.name.price_per_unit
        return price_per_unit
    