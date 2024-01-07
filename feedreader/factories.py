import factory

from .models import Entry, Feed, Group


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Group %s" % n)


class FeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feed

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: "Feed %s" % n)
    xml_url = factory.Sequence(lambda n: "feed-%s-xmlurl" % n)
    link = factory.Sequence(lambda n: "feed-%s-link" % n)
    description = factory.Sequence(lambda n: "Feed %s description" % n)


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry

    id = factory.Sequence(lambda n: n)
    feed = factory.SubFactory(FeedFactory)
    title = factory.Sequence(lambda n: "Entry %s" % n)
    link = factory.Sequence(lambda n: "entry-%s-link" % n)
    description = factory.Sequence(lambda n: "Entry %s description" % n)
