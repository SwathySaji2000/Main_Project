# from django import forms
# from .models import Bookings

# class BookingForm(forms.ModelForm):
#     ROOM_TYPE_CHOICES = [
#         ('ac', 'AC'),
#         ('non_ac', 'Non-AC'),
#     ]

#     room_type = forms.ChoiceField(choices=ROOM_TYPE_CHOICES)

#     class Meta:
#         model = Bookings
#         fields = ['date_start', 'treatment_type', 'food_plan', 'number_of_days']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['date_start'].widget.attrs.update({'class': 'datepicker'})
        

