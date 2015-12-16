from django import forms
from lib.multiupload.fields import MultiFileField
from .models import MontageElementContainer, MontageElement

class MontageCreateForm(forms.Form):
  	title = forms.CharField(label='Montage title',
                          	max_length=1000,
                          	widget=forms.TextInput(attrs={'placeholder': 'Montage Name',
                                                          'class': 'form-control',
                                                          'aria-describedby': 'basic-addon1'}))
  	files = MultiFileField(min_num = 1,
    					   max_num = 50,
    					   label = 'Select a file',
    					   help_text = 'max. 42 megabytes')
