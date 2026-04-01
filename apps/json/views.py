from django.db.models import F, Sum, Window
from django.db.models.functions import RowNumber, ExtractYear
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.json.models import RepositoryLanguage
from .serializers import YearTopLanguagesSerializer


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

        data = {}
        for item in queryset:
            year = item['year']
            if year not in data:
                data[year] = {'year': year, 'languages': []}
            data[year]['languages'].append(item)

        data_by_year = list(data.values())
        serializer = YearTopLanguagesSerializer(data_by_year, many=True)

        return Response(serializer.data)
