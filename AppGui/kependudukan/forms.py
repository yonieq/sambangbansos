from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit
from django import forms
from django.forms import ModelForm

from Database.models import Keluarga, Warga, NON_AKTIF_STATUS, Desa, WARGA_STATUS


class WargaForms(forms.Form):
    Nik = forms.IntegerField()
    Nama = forms.CharField(max_length=100)
    TmptLahir = forms.CharField(max_length=10)
    TglLahir = forms.DateField()
    Alamat = forms.CharField(max_length=150)
    Rt = forms.IntegerField()
    Rw = forms.IntegerField()
    Desa = forms.ModelChoiceField(queryset=Desa.objects.all().order_by('id'))
    Keluarga = forms.ModelChoiceField(queryset=Keluarga.objects.all().order_by('NomerKK'))
    NikValid = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(WargaForms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'


class WargaFormsUpdate(ModelForm):
    class Meta:
        model = Warga
        fields = ['Nik', 'Nama', 'TmpLahir', 'TglLahir', 'Alamat', 'Rt', 'Rw', 'Desa', 'Keluarga', 'NikValid']

    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column(Field('Nik'))),
            Row(Column(Field('Nama'))),
            Row(Column(Field('TmpLahir'))),
            Row(Column(Field('TglLahir'))),
            Row(Column(Field('Alamat'))),
            Row(Column(Field('Rt')), Column(Field('Rw'))),
            Row(Column(Field('Desa'))),
            Row(Column(Field('Keluarga'))),
            Row(Column(Field('NikValid'))),
            Submit('submit', 'Simpan', css_class='btn-theme'),
        )

        self.helper.form_show_labels = True


class KeluargaForms(forms.Form):
    NomerKK = forms.IntegerField()
    Alamat = forms.CharField(max_length=150)
    Rt = forms.IntegerField()
    Rw = forms.IntegerField()
    Desa = forms.ModelChoiceField(queryset=Desa.objects.all().order_by('id'))

    def __init__(self, *args, **kwargs):
        super(KeluargaForms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'


class KeluargaFormsUpdate(ModelForm):
    class Meta:
        model = Keluarga
        fields = ['NomerKK', 'Alamat', 'Rt', 'Rw', 'Desa']

    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column(Field('NomerKK'))),
            Row(Column(Field('Alamat'))),
            Row(Column(Field('Rt')), Column(Field('Rw'))),
            Row(Column(Field('Desa'))),
            Submit('submit', 'Simpan', css_class='btn-theme'),
        )

        self.helper.form_show_labels = True


class RevisiNikForms(ModelForm):
    class Meta:
        model = Warga
        fields = ['Nik', 'Nama', 'TmpLahir', 'TglLahir', 'Alamat', 'Rt',
                  'Rw']  # , 'Nama', 'TmpLahir', 'TglLahir', 'Alamat', 'Rt', 'Rw', 'Keluarga'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column(Field('Nik')), Column(Field('Nama', readonly=True))),
            Row(Column(Field('TmpLahir', readonly=True)), Column(Field('TglLahir', readonly=True))),
            Row(Column(Field('Alamat', readonly=True))),
            Row(Column(Field('Rt', readonly=True)), Column(Field('Rw', readonly=True))),
            # Row(Column(Field('Keluarga', readonly=True))),
            Submit('submit', 'Simpan', css_class='btn-theme'),
        )

        self.helper.form_show_labels = True


class NonAktifStatusForms(forms.Form):
    Nik = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Nama = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Alamat = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    Status = forms.ChoiceField(choices=NON_AKTIF_STATUS)

    def __init__(self, *args, **kwargs):
        super(NonAktifStatusForms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
