from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from movies.models import Filmwork, Role


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def aggregate_person(self, role: Role):
        return ArrayAgg(
            'persons__full_name',
            distinct=True,
            filter=Q(personfilmwork__role=role)
        )

    def get_queryset(self):
        queryset = self.model.objects.values().prefetch_related('Genre', 'Person').annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=self.aggregate_person(Role.ACTOR),
            directors=self.aggregate_person(Role.DIRECTOR),
            writers=self.aggregate_person(Role.WRITER)
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        count = paginator.count
        total_pages = paginator.num_pages
        prev = page.previous_page_number() if page.has_previous() else None
        next = page.next_page_number() if page.has_next() else None
        results = list(queryset.values())
        return {'count': count,
                'total_pages': total_pages,
                'prev': prev,
                'next': next,
                'results': results
                }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return kwargs['object']
