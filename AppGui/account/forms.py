from django import forms


class AccountProfileForms(forms.Form):
    FirstName = forms.CharField(max_length=100)
    LastName = forms.CharField(max_length=100)
    Email = forms.EmailField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(AccountProfileForms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'


class AccountPasswordForms(forms.Form):
    Password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    RePassword = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(AccountPasswordForms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'