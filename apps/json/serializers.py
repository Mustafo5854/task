from rest_framework import serializers


class LanguageSizeSerializer(serializers.Serializer):
    language = serializers.CharField()
    size = serializers.IntegerField()


class YearTopLanguagesSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    languages = serializers.SerializerMethodField()

    def get_languages(self, obj):
        return [
            {'language': item['language__name'], 'size': item['total_size']}
            for item in obj['languages']
        ]
