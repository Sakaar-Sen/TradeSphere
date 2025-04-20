from django import forms
from .models import Conversation, ConversationMessage


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'w-full border border-gray-800 rounded-md p-2', 'placeholder': 'Type your message here...'}),
        }
        