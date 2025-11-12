# appfinanciero/forms.py
from django import forms
from .models import Product, InventoryMove, Employee, PayrollConfig, TaxBracket

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['codigo', 'nombre', 'unidad']

class InventoryMoveForm(forms.ModelForm):
    class Meta:
        model = InventoryMove
        fields = ['producto', 'fecha', 'tipo', 'cantidad', 'costo_unitario', 'referencia']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['activo', 'dui', 'nombre', 'salario_mensual', 'fecha_ingreso']
        widgets = {'fecha_ingreso': forms.DateInput(attrs={'type': 'date'})}

class PayrollConfigForm(forms.ModelForm):
    class Meta:
        model = PayrollConfig
        fields = ['nombre', 'isss_empleado_pct', 'isss_techo', 'afp_empleado_pct']

class TaxBracketForm(forms.ModelForm):
    class Meta:
        model = TaxBracket
        fields = ['desde', 'hasta', 'cuota_fija', 'tasa_exceso_pct']
        
class EntradaRapidaForm(forms.Form):
    cantidad = forms.DecimalField(label="Cantidad", max_digits=14, decimal_places=4, min_value=0.0001)
    costo_unitario = forms.DecimalField(label="Costo unitario", max_digits=14, decimal_places=4, min_value=0.0001)
    referencia = forms.CharField(label="Referencia", required=False, max_length=120)

class SalidaRapidaForm(forms.Form):
    cantidad = forms.DecimalField(label="Cantidad", max_digits=14, decimal_places=4, min_value=0.0001)
    referencia = forms.CharField(label="Referencia", required=False, max_length=120)