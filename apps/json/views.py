from collections import defaultdict
from django.db.models import Sum
from django.db.models.functions import ExtractYear
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.json.models import RepositoryLanguage


class TopLanguagesByYearView(APIView):
    def get(self, request):
        queryset = (
            RepositoryLanguage.objects
            .annotate(year=ExtractYear('repo__created_at'))
            .values('year', 'language__name')
            .annotate(total_size=Sum('size'))
            .order_by('-year', '-total_size')
        )

        data = defaultdict(list)
        for item in queryset:
            year = item['year']
            if len(data[year]) < 5:
                data[year].append({
                    'language': item['language__name'],
                    'size': item['total_size']
                })

        return Response(data)