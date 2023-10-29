from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type Your Question Here', 'style': 'font-weight: 200;'}))
