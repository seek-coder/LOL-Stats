from django import forms

class BusquedaInvocadorForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Invocador', max_length=100)
    tag_line = forms.CharField(label='Tag Line', max_length=100)
