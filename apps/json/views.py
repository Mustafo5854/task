from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.json.models import RepositoryLanguage


class TopLanguagesByYearView(APIView):

    def get(self, request):
        data = defaultdict(lambda: defaultdict(int))

        queryset = RepositoryLanguage.objects.select_related('repo', 'language')

        for rl in queryset:
            year = rl.repo.created_at.year
            lang = rl.language.name
            data[year][lang] += 1

        result = {}

        for year in sorted(data.keys(), reverse=True):
            langs = data[year]
            sorted_langs = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:5]
            result[year] = [
                {"language": lang, "count": count}
                for lang, count in sorted_langs
            ]
        return Response(result)