import factory

from django.utils import timezone

from .models import BlogPage


class BlogPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogPage

    title = factory.Sequence(lambda n: "Blog Page %s" % n)
    slug = factory.Sequence(lambda n: "blog-page-%s" % n)
    updated = factory.LazyFunction(timezone.now)
    content = factory.Faker("text", max_nb_chars=50)
    published = factory.LazyFunction(timezone.now)
