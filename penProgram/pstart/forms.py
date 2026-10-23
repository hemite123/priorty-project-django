from django import forms

class InputKriteria(forms.Form):
    id_kriteria = forms.TextInput(max_lenght=100)
    nama_tipe = forms.TextInput(max_lenght=100)