import csv
import itertools

from django.core.management.base import BaseCommand

from elections.models import PostElection
from results.models import ResultEvent

'''
Import GE2017 declaration times as estimated by PA. One-off script,
don't reuse without fixing the time hack below.
CSV file available here:
https://docs.google.com/spreadsheets/d/1o-P27WYPRV934sgCwCBANr4a36KpJQwtwUnPdczAaI8/edit?usp=sharing
Original source:
http://election.pressassociation.com/Declaration_times/general_2017_by_name.php
'''


class Command(BaseCommand):
    help = "Import predicted declaration times from PA"

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            help='Path to the file with expected declaration times'
        )

    def get_postelections(self, query):
        return PostElection.objects.filter(
            election_id='385',
            post__area_name=query)

    def get_constituency(self, constituency):
        matches = {
            'Ashton Under Lyne': 'Ashton-under-Lyne',
            'Ynys Mon': 'Ynys Môn'
        }
        if constituency in matches:
            constituency = matches[constituency]
        constituency = constituency.replace('&', 'and').strip()
        constituency = constituency.replace("Hull", "Kingston upon Hull")
        postelection = self.get_postelections(constituency)
        if not postelection:
            c = constituency.split()
            c.reverse()
            postelection = self.get_postelections(' '.join(c))
            if not postelection:
                c = constituency.split()
                c[0] = c[0] + ','
                postelection = self.get_postelections(' '.join(c))
                if not postelection:
                    if ', ' in constituency:
                        c = constituency.split(',')
                        postelection = self.get_postelections(
                            ' '.join([c[1], c[0]]).strip())
                    if not postelection:
                        c = constituency.split()
                        for perm in itertools.permutations(c):
                            if postelection:
                                break
                            postelection = self.get_postelections(
                                ' '.join(perm))
        return postelection

    def handle(self, *args, **options):
        with open(options['filename'], 'r') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                postelection = self.get_constituency(row['constituency'])[0]
                # Hack for GE2017!
                if row['time'].startswith('23'):
                    t = '2016-06-08 %s' % (row['time'])
                else:
                    t = '2016-06-09 %s' % (row['time'])
                resultevent, _ = ResultEvent.objects.update_or_create(
                    post_election=postelection,
                    defaults={
                        'expected_declaration_time': t
                    })