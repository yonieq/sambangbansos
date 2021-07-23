from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.forms import ModelForm
from django import forms

from Database.models import PenerimaBantuan, Bantuan, Keluarga


# class BantuanForms(ModelForm):
#     class Meta:
#         model = PenerimaBantuan
#         fields = ['Bantuan', 'Keluarga']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(Column('Keluarga')),
#             Row(Column('Bantuan')),
#             Submit('submit', 'Simpan', css_class='btn-theme'),
#         )
#
#         self.helper.form_show_labels = True

class BantuanForms(forms.Form):
    Bantuan = forms.ModelChoiceField(queryset=Bantuan.objects.all().order_by('Nama'))
    Keluarga = forms.ModelChoiceField(queryset=Keluarga.objects.all().order_by('NomerKK'))
    Status = forms.ModelChoiceField(queryset=PenerimaBantuan.objects.all().order_by('Status'))
    TglPengajuan = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(BantuanForms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
