from django.views.generic import DetailView
from django.http import Http404
from django.db.models import Prefetch
from django.utils.html import strip_tags

from .models import Person, PersonPost
from elections.models import PostElection
from leaflets.models import Leaflet


class PersonMixin(object):
    def get_object(self, queryset=None):
        return self.get_person(queryset)

    def get_person(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(
            ynr_id=pk).select_related(
                'cv'
            ).prefetch_related(
                Prefetch(
                    'personpost_set',
                    queryset=PersonPost.objects.all().select_related(
                        'election', 'post', 'party')
                )
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})

        obj.current_personposts = PersonPost.objects.filter(
            person=obj, election__current=True).select_related(
                'party',
                'post',
                'election',
            )
        obj.leaflets = Leaflet.objects.filter(person=obj) \
            .order_by('-date_uploaded_to_electionleaflets')[:3]

        return obj


class PersonView(DetailView, PersonMixin):
    model = Person

    def get_object(self, queryset=None):
        obj = self.get_person(queryset)

        obj.past_personposts = PersonPost.objects.filter(
            person=obj, election__current=False).select_related(
                'party',
                'post',
                'election'
            )
        obj.personpost = None
        if obj.current_personposts:
            obj.personpost = obj.current_personposts[0]
        elif obj.past_personposts:
            obj.personpost = obj.past_personposts[0]
        obj.title = self.get_title(obj)
        obj.intro = self.get_intro(obj)
        obj.text_intro = strip_tags(obj.intro)

        return obj

    def get_title(self, person):
        title = person.name
        if person.personpost:
            title += ' for ' + person.personpost.post.label + ' in the '
            title += person.personpost.election.name
        return title

    def get_intro(self, person):
        intro = [person.name]
        if person.current_personposts:
            intro.append('is')
        elif person.past_personposts:
            intro.append('was')
        if person.personpost:
            party = person.personpost.party
            if party:
                if party.party_name == "Independent":
                    intro.append('an independent candidate')
                elif party.party_name == "Speaker seeking re-election":
                    intro.append('the Speaker seeking re-election')
                else:
                    intro.append('the')
                    str = '<a href="' + party.get_absolute_url() + '">'
                    str += party.party_name + '</a> candidate'
                    intro.append(str)
            else:
                intro.append('a candidate')
            intro.append('in')
            if person.personpost.post.organization ==\
                    'House of Commons of the United Kingdom':
                intro.append('the constituency of')
            try:
                postelection = PostElection.objects.get(
                    post=person.personpost.post,
                    election=person.personpost.election)
                str = '<a href="' + postelection.get_absolute_url() + '">'
                str += person.personpost.post.label + '</a>'
            except PostElection.DoesNotExist:
                str = person.personpost.post.label
            str += ' in the <a href="'
            str += person.personpost.election.get_absolute_url()
            str += '">' + person.personpost.election.name + '</a>'
            intro.append(str)
        return ' '.join(intro)


class EmailPersonView(PersonMixin, DetailView):
    template_name = "people/email_person.html"
    model = Person
