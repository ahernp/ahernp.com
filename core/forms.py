from django import forms

IMAGE = "img"
THUMBNAIL = "img/thumbnail"

FILE_TYPE_CHOICES = ((IMAGE, "Image"), (THUMBNAIL, "Thumbnail"))


class UploadForm(forms.Form):
    upload_file = forms.FileField()
    upload_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES, initial=IMAGE)
