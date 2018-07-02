from rest_framework import serializers

from mpages.models import Page

class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "content", "content_as_html"]
