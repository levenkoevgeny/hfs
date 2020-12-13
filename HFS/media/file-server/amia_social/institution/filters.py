import django_filters
from institution.models import Institution, Vacancy


class VacancyFilterForProfile(django_filters.FilterSet):

    institution = django_filters.ModelMultipleChoiceFilter(queryset=Institution.objects.all())
    vacancy = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Vacancy
        fields = [
            'institution',
            'vacancy',
        ]