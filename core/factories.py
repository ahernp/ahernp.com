import factory

from django.utils import timezone

from .models import Log


class LogFactory(factory.Factory):
    class Meta:
        model = Log

    level = factory.Sequence(lambda n: "level%s" % n)
    msg = factory.Faker("text", max_nb_chars=50)
    datetime = factory.LazyFunction(timezone.now)
