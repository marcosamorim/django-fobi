from django.forms.fields import CharField
from django.forms.widgets import HiddenInput  # , TextInput
from django.utils.translation import ugettext_lazy as _

from fobi.base import FormFieldPlugin, form_element_plugin_registry, get_theme

from . import UID
from .forms import HiddenInputForm

__title__ = 'fobi.contrib.plugins.form_elements.fields.' \
            'hidden.fobi_form_elements'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('HiddenInputPlugin',)

theme = get_theme(request=None, as_instance=True)


class HiddenInputPlugin(FormFieldPlugin):
    """Hidden field plugin."""

    uid = UID
    name = _("Hidden")
    group = _("Fields")
    form = HiddenInputForm
    is_hidden = True

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):
        """Get form field instances."""
        field_kwargs = {
            'label': self.data.label,
            'initial': self.data.initial,
            'required': self.data.required,
            'widget': HiddenInput(
                attrs={'class': theme.form_element_html_class}
            ),
        }
        if self.data.max_length:
            field_kwargs['max_length'] = self.data.max_length

        return [(self.data.name, CharField, field_kwargs)]
        # return [(self.data.name, (CharField, TextInput), kwargs)]


form_element_plugin_registry.register(HiddenInputPlugin)
