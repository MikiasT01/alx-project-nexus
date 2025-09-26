from rest_framework import serializers
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'created_at', 'expiry', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(poll=poll, **option_data)
        return poll

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['option']

class ResultSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    text = serializers.CharField()
    vote_count = serializers.IntegerField()