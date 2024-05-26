from django import forms
from .models import PropertyListing, Meeting

class PropertyListingForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Title'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Property Description'})
    )
    area = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Property Area'})
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Property Price'})
    )
    property_type = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Type'})
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'location-input', 'placeholder': 'Click to select location'})
    )

    class Meta:
        model = PropertyListing
        fields = [
            'title', 
            'description', 
            'location', 
            'area', 
            'price', 
            'property_type',
        ]

    def save(self, commit=True, owner=None):
        listing = super(PropertyListingForm, self).save(commit=False)
        if owner:
            listing.owner = owner
        if commit:
            listing.save()
        return listing
    
    def delete(self, commit=True):
        listing = super(PropertyListingForm, self).save(commit=False)
        if commit:
            listing.is_active = False
            listing.save()
        return listing
    
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['landowner', 'date', 'time']
        widgets = {
            'date': forms.SelectDateWidget(),
            'time': forms.TimeInput(format='%H:%M'),
        }
