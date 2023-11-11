from rest_framework import serializers


class DurationValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if int(value) > 120:
            raise serializers.ValidationError('Duration must be less than 120 seconds')
        if int(value) < 1:
            raise serializers.ValidationError('Duration cannot be so short')
