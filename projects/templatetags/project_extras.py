from django import template

register = template.Library()


@register.inclusion_tag('projects/common/field_wrapper.html')
def field(form_field, show_label=False):
    if show_label:
        label_tag = form_field.label_tag()
    else:
        label_tag = form_field.label_tag(attrs={'class': 'sr-only'})
    return {'form_field': form_field, 'label_tag': label_tag}


