import datetime
import unittest

from django.utils import timezone

from .factories import LogFactory


class LogTestCase(unittest.TestCase):
    def test_recent_logs(self):
        log = LogFactory.create()
        self.assertEqual(log.recent(), True, "Newly created log is recent")

        log.datetime = timezone.now() - datetime.timedelta(days=2)
        self.assertEqual(log.recent(), False, "Two day old log is not recent")
