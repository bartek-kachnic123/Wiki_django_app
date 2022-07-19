
from django.forms import Form, CharField, Textarea, TextInput


class PageForm(Form):
    title = CharField(widget=TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px' }), label="Title", max_length=50)
    content = CharField(widget=Textarea(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px'}), label="Content", max_length=1000)

    def disable_title(self):
        self.fields['title'].disabled = True