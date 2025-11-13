# appfinanciero/forms.py
from django import forms
from django.forms import widgets as django_widgets
from .models import Product, InventoryMove, Employee, PayrollConfig, TaxBracket

class BootstrapWidgetMixin:
    """
    Añade clases Bootstrap a los widgets de un formulario.
    - inputs => 'form-control'
    - selects => 'form-select'
    - textarea => 'form-control'
    - checkbox => 'form-check-input'
    - file => 'form-control'
    """
    input_class = "form-control"
    select_class = "form-select"
    textarea_class = "form-control"
    checkbox_class = "form-check-input"
    file_class = "form-control"

    def _apply_bootstrap(self):
        for name, field in self.fields.items():
            widget = field.widget
            # preserva attrs existentes
            attrs = dict(getattr(widget, "attrs", {}) or {})

            # Determina clase por tipo de widget (usar clases concretas)
            if isinstance(widget, (
                django_widgets.TextInput,
                django_widgets.NumberInput,
                django_widgets.EmailInput,
                django_widgets.URLInput,
                django_widgets.PasswordInput,
                django_widgets.HiddenInput,
                django_widgets.DateInput,
                django_widgets.DateTimeInput,
                django_widgets.TimeInput,
            )):
                attrs.setdefault("class", self.input_class)
            elif isinstance(widget, (django_widgets.Select, django_widgets.SelectMultiple)):
                attrs.setdefault("class", self.select_class)
            elif isinstance(widget, django_widgets.Textarea):
                attrs.setdefault("class", self.textarea_class)
            elif isinstance(widget, django_widgets.CheckboxInput):
                attrs.setdefault("class", self.checkbox_class)
            elif isinstance(widget, django_widgets.FileInput):
                attrs.setdefault("class", self.file_class)
            else:
                # fallback seguro
                attrs.setdefault("class", self.input_class)

            widget.attrs = attrs

    def _maybe_apply(self):
        try:
            self._apply_bootstrap()
        except Exception:
            # no romper si hay algo raro; mejor dejar sin clases que caer
            pass


# -------------------------
# Model forms
# -------------------------
class ProductForm(BootstrapWidgetMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['codigo', 'nombre', 'unidad']
        widgets = {
            'codigo': forms.TextInput(attrs={'placeholder': 'Ej. P001'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del producto'}),
            'unidad': forms.TextInput(attrs={'placeholder': 'unid'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._maybe_apply()


class InventoryMoveForm(BootstrapWidgetMixin, forms.ModelForm):
    class Meta:
        model = InventoryMove
        fields = ['producto', 'fecha', 'tipo', 'cantidad', 'costo_unitario', 'referencia']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'cantidad': forms.NumberInput(attrs={'step': 'any'}),
            'costo_unitario': forms.NumberInput(attrs={'step': 'any'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._maybe_apply()


class EmployeeForm(BootstrapWidgetMixin, forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['activo', 'dui', 'nombre', 'salario_mensual', 'fecha_ingreso']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'salario_mensual': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._maybe_apply()


class PayrollConfigForm(BootstrapWidgetMixin, forms.ModelForm):
    class Meta:
        model = PayrollConfig
        fields = ['nombre', 'isss_empleado_pct', 'isss_techo', 'afp_empleado_pct']
        widgets = {
            'isss_empleado_pct': forms.NumberInput(attrs={'step': '0.01'}),
            'isss_techo': forms.NumberInput(attrs={'step': '0.01'}),
            'afp_empleado_pct': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._maybe_apply()


class TaxBracketForm(BootstrapWidgetMixin, forms.ModelForm):
    class Meta:
        model = TaxBracket
        fields = ['desde', 'hasta', 'cuota_fija', 'tasa_exceso_pct']
        widgets = {
            'desde': forms.NumberInput(attrs={'step': '0.01'}),
            'hasta': forms.NumberInput(attrs={'step': '0.01'}),
            'cuota_fija': forms.NumberInput(attrs={'step': '0.01'}),
            'tasa_exceso_pct': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._maybe_apply()


# -------------------------
# Simple forms (non-Model)
# -------------------------
class EntradaRapidaForm(BootstrapWidgetMixin, forms.Form):
    cantidad = forms.DecimalField(
        label="Cantidad", max_digits=14, decimal_places=4, min_value=0.0001,
        widget=forms.NumberInput(attrs={'step': 'any'})
    )
    costo_unitario = forms.DecimalField(
        label="Costo unitario", max_digits=14, decimal_places=4, min_value=0.0001,
        widget=forms.NumberInput(attrs={'step': 'any'})
    )
    referencia = forms.CharField(label="Referencia", required=False, max_length=120,
                                 widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._maybe_apply()


class SalidaRapidaForm(BootstrapWidgetMixin, forms.Form):
    cantidad = forms.DecimalField(
        label="Cantidad", max_digits=14, decimal_places=4, min_value=0.0001,
        widget=forms.NumberInput(attrs={'step': 'any'})
    )
    referencia = forms.CharField(label="Referencia", required=False, max_length=120,
                                 widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._maybe_apply()
