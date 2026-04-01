from django.db.models import F, Sum, Window
from django.db.models.functions import RowNumber, ExtractYear
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.json.models import RepositoryLanguage
from .serializers import YearTopLanguagesSerializer
from django.contrib.postgres.aggregates import ArrayAgg


class TopLanguagesByYearView(APIView):
    def get(self, request):
        queryset = (
            RepositoryLanguage.objects
            .annotate(year=ExtractYear('repo__created_at'))
            .values('year', 'language__name')
            .annotate(total_size=Sum('size'))
            .annotate(
                rank=Window(
                    expression=RowNumber(),
                    partition_by=[F('year')],
                    order_by=F('total_size').desc()
                )
            )
            .filter(rank__lte=5)
            .order_by('-year', '-total_size')
        )

        aggregated = (
            queryset.values('year').annotate(
                languages=ArrayAgg(F('language__name')),
                sizes=ArrayAgg(F('total_size')))
            .order_by('-year')
        )

        serializer = YearTopLanguagesSerializer(aggregated, many=True)
        return Response(serializer.data)
