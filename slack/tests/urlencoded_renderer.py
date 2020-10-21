from urllib.parse import urlencode

from rest_framework.renderers import BaseRenderer


class UrlencodedRenderer(BaseRenderer):
    media_type = 'application/x-www-form-urlencoded'
    format = 'urlencoded'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return urlencode(data)