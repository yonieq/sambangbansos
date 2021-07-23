from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit
from django.forms import ModelForm

from Database.models import Warga


class RevisiNikForms(ModelForm):
    class Meta:
        model = Warga
        fields = ['Nik', 'Nama', 'TmpLahir', 'TglLahir', 'Alamat', 'Rt', 'Rw',
                  'Keluarga']  # , 'Nama', 'TmpLahir', 'TglLahir', 'Alamat', 'Rt', 'Rw', 'Keluarga'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('Nik')),
            Field('Nama', type='hidden'),
            Field('TmpLahir', type='hidden'),
            Field('TglLahir', type='hidden'),
            Field('Alamat', type='hidden'),
            Field('Rt', type='hidden'),
            Field('Rw', type='hidden'),
            Field('Keluarga', type='hidden'),
            Submit('submit', 'Simpan', css_class='btn-theme'),
        )

        self.helper.form_show_labels = True
