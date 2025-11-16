from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Uso en templates:
      {{ form.mi_campo|add_class:"form-control" }}
    Devuelve el widget con el atributo class añadido.
    """
    try:
        # Si field es un BoundField -> as_widget con attrs
        return field.as_widget(attrs={"class": css_class})
    except Exception:
        # fallback — si algo falla devolvemos el field bruto
        return field
