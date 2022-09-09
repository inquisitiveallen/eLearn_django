from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp.models import Order, Student


class InterestForm(forms.Form):
    CHOICES = [(1, 'Yes'), (0, 'No')]
    interested = forms.CharField(label='Interested', widget=forms.RadioSelect(choices=CHOICES))
    levels = forms.IntegerField(label='Levels', initial=1)
    comments = forms.CharField(label='Additional Comments', widget=forms.Textarea, required=False)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student','course','levels','order_date']
        student = forms.ChoiceField(widget=forms.RadioSelect())
        order_date = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))

class RegisterForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ["username", "first_name", "last_name", "password1", "password2"]
