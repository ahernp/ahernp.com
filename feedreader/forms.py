from django import forms


class ToggleEntryReadForm(forms.Form):
    feed_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    entry_id = forms.IntegerField(widget=forms.HiddenInput())
