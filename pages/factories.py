import factory

from django.utils import timezone

from .models import Page


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page

    title = factory.Sequence(lambda n: "Page %s" % n)
    slug = factory.Sequence(lambda n: "page-%s" % n)
    updated = factory.LazyFunction(timezone.now)
    content = factory.Faker("text", max_nb_chars=50)
