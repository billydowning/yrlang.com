from django import forms
from users.models import CustomUser
from .models import Review, ReportAProblem
class UserSearchFrom(forms.ModelForm):


    class Meta:
        model = CustomUser
        fields = ['country',]

    def __init__(self, *args,**kwargs):
        super(UserSearchFrom, self).__init__(*args,**kwargs)
        self.fields['country'].empty_label = 'select country'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 mr-sm-2'

class BookingReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["review_choice_1", "review_choice_2", "review_choice_3", 'description',]
        labels = {
            "review_choice_1":'options 1',
            "review_choice_2":'options 2',
            "review_choice_3":'options 3'
        }

    def __init__(self, *args, **kwargs):
         super(BookingReviewForm, self).__init__(*args, **kwargs)
         self.fields['review_choice_1'].required = True
         self.fields['review_choice_2'].required = True
         self.fields['review_choice_3'].required = True


class BoookingAndAppointmentComplainForm(forms.ModelForm):

    class Meta:
        model = ReportAProblem
        fields = ['description']
        help_texts = {
         'description': 'Describe your Problem the Some Words'
        }

    def __init__(self, *args, **kwargs):
        super(BoookingAndAppointmentComplainForm, self).__init__( *args, **kwargs)
        self.fields['description'].required =True