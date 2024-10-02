from django import forms
from django.forms import inlineformset_factory
from app import models


class InventoryForm(forms.ModelForm):
    class Meta:
        model = models.Inventory
        fields = ['name', 'quantity', 'location']
    
class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = ['name']

class RecipeItemForm(forms.ModelForm):
    class Meta:
        model = models.RecipeItem
        fields = ['inventory', 'quantity', 'deleted']
        widgets = {
            'quantity': forms.Select(choices=[(i, i) for i in range(1, 21)]),
            'deleted': forms.HiddenInput(),
        }


RecipeItemFormSet = inlineformset_factory(
    models.Recipe, models.RecipeItem, form=RecipeItemForm, extra=1, max_num = 20, can_delete=False
)

RecipeItemFormSetForEdit = inlineformset_factory(
    models.Recipe, 
    models.RecipeItem, 
    form=RecipeItemForm, 
    extra=0,
    can_delete=False
)



RecipeItemFormSetForCreate = inlineformset_factory(
    models.Recipe, 
    models.RecipeItem, 
    form=RecipeItemForm, 
    extra=1,
    can_delete=False
)

class StandardInventoryCSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class LocationCSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class RecipeCSVUploadForm(forms.Form):
    csv_file = forms.FileField()


class RecipeCreationForm(forms.Form):
    recipes = forms.ModelMultipleChoiceField(queryset=models.Recipe.objects.all(), widget=forms.SelectMultiple)
    quantity = forms.IntegerField(min_value=1, max_value=20)