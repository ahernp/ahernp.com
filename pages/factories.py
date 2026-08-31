import factory
from django.utils import timezone

from .models import Page


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page

    title = factory.Sequence(lambda n: f"Page {n}")
    slug = factory.Sequence(lambda n: f"page-{n}")
    updated = factory.LazyFunction(timezone.now)
    content = factory.Faker("text", max_nb_chars=50)
