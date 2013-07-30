from django import forms

class UpdateAccountForm(forms.Form):
    Email = forms.EmailField()
    FirstName = forms.CharField()
    LastName = forms.CharField()
    HomePhone = forms.CharField()
    CellPhone = forms.CharField(required=False)
    WorkPhone = forms.CharField(required=False)
    AllowReceiveEmails = forms.BooleanField(required=False)
    AllowReceiveSMS = forms.BooleanField(required=False)
    Street1 = forms.CharField()
    Street2 = forms.CharField(required=False)
    City = forms.CharField()
    State = forms.CharField()
    ZipCode = forms.CharField()

