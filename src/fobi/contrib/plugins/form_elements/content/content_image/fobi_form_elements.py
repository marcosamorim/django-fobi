from uuid import uuid4

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from nonefield.fields import NoneField

from fobi.base import FormElementPlugin, form_element_plugin_registry
from fobi.helpers import delete_file, clone_file

from . import UID
from .forms import ContentImageForm
from .helpers import get_crop_filter
from .settings import (
    FIT_METHOD_FIT_WIDTH, FIT_METHOD_FIT_HEIGHT, IMAGES_UPLOAD_DIR
)

__title__ = 'fobi.contrib.plugins.form_elements.content.content_image.' \
            'fobi_form_elements'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('ContentImagePlugin',)


class ContentImagePlugin(FormElementPlugin):
    """Content image plugin."""

    uid = UID
    name = _("Content image")
    group = _("Content")
    form = ContentImageForm

    def post_processor(self):
        """Post process data.

        Always the same.
        """
        self.data.name = "{0}_{1}".format(self.uid, uuid4())

    def delete_plugin_data(self):
        """Delete uploaded file."""
        delete_file(self.data.file)

    def clone_plugin_data(self, entry):
        """Clone plugin data.

        Clone plugin data, which means we make a copy of the original image.

        TODO: Perhaps rely more on data of ``form_element_entry``?
        """
        cloned_image = clone_file(
            IMAGES_UPLOAD_DIR, self.data.file, relative_path=True
        )
        return self.get_cloned_plugin_data(update={'file': cloned_image})

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):
        """Get form field instances."""
        width, height = self.data.size.split('x')
        crop = get_crop_filter(self.data.fit_method)

        if FIT_METHOD_FIT_WIDTH == self.data.fit_method:
            thumb_size = (width, 0)
        elif FIT_METHOD_FIT_HEIGHT == self.data.fit_method:
            thumb_size = (0, height)
        else:
            thumb_size = (width, height)

        context = {
            'plugin': self,
            'MEDIA_URL': settings.MEDIA_URL,
            'crop': crop,
            'thumb_size': thumb_size
        }
        rendered_image = render_to_string('content_image/render.html', context)

        field_kwargs = {
            'initial': rendered_image,
            'required': False,
            'label': '',
        }

        return [(self.data.name, NoneField, field_kwargs)]


form_element_plugin_registry.register(ContentImagePlugin)
