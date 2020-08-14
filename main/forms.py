from django import forms
from users.models import CustomUser

class UserSearchFrom(forms.ModelForm):


    class Meta:
        model = CustomUser
        fields = ['country',]

    def __init__(self, *args,**kwargs):
        super(UserSearchFrom, self).__init__(*args,**kwargs)
        self.fields['country'].empty_label = 'select country'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 mr-sm-2'

