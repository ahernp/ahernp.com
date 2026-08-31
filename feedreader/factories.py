import factory

from .models import Entry, Feed, Group


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"Group {n}")


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feed

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: f"Feed {n}")
    xml_url = factory.Sequence(lambda n: f"feed-{n}-xmlurl")
    link = factory.Sequence(lambda n: f"feed-{n}-link")
    description = factory.Sequence(lambda n: f"Feed {n} description")


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry

    id = factory.Sequence(lambda n: n)
    feed = factory.SubFactory(FeedFactory)
    title = factory.Sequence(lambda n: f"Entry {n}")
    link = factory.Sequence(lambda n: f"entry-{n}-link")
    description = factory.Sequence(lambda n: f"Entry {n} description")
