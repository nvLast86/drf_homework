from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = dict(value).get(self.field)
        if url:
            if 'youtube.com' not in str(url):
                raise ValidationError('Это не YouTube')
