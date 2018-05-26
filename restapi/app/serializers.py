from rest_framework import serializers
from app.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from app import models

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

class AuthSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class ArtileSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    subtitle = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=200)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def create(self, validated_data):
        return models.Artile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title =validated_data.get('title', instance.title)
        instance.subtitle = validated_data.get('subtitle', instance.subtitle)
        instance.body = validated_data.get('body', instance.body)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.save()
        return instance


class CommitSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=200)
    text = serializers.CharField()
    # atrtle = serializers.PrimaryKeyRelatedField(queryset=models.Artile.objects.all())
    create_time = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return models.Commit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.artile = validated_data.get('artile', instance.artile)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.save()
        return instance

class ArtileSerializer2(serializers.Serializer):

    commits = CommitSerializer(many=True)

    title = serializers.CharField(max_length=200)
    subtitle = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=200)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def create(self, validated_data):
        commits = validated_data.pop('commits')
        artile = models.Artile.objects.create(**validated_data)
        for c in commits:
            models.Commit.objects.create(atrtle=artile, **c)
        return artile

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.artile = validated_data.get('artile', instance.artile)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.save()
        return instance