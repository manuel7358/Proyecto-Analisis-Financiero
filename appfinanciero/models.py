from django.db import models

# Create your models here.
# appfinanciero/models.py
from django.db import models
from django.utils import timezone
from decimal import Decimal

# =====================
# CONFIGURACIÓN NÓMINA
# =====================
class PayrollConfig(models.Model):
    """Parámetros editables desde el admin."""
    nombre = models.CharField(max_length=100, default='Parámetros El Salvador')
    isss_empleado_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('3.00'))     # %
    isss_techo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))        # salario tope p/ISSS
    afp_empleado_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('7.25'))      # %
    # Tabla renta: usa tramos almacenados abajo
    def __str__(self):
        return self.nombre

class TaxBracket(models.Model):
    """Tramos de renta mensual: editable en admin.
    Cálculo: impuesto = cuota_fija + (exceso * tasa_exceso_pct/100)
    """
    desde = models.DecimalField(max_digits=10, decimal_places=2)
    hasta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # None = infinito
    cuota_fija = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tasa_exceso_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    def __str__(self):
        h = '∞' if self.hasta is None else self.hasta
        return f"{self.desde} - {h}"

# =========
# INVENTARIO
# =========
class Product(models.Model):
    codigo = models.CharField(max_length=30, unique=True, default="TEMP")
    nombre = models.CharField(max_length=120)
    unidad = models.CharField(max_length=20, default='unid')
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class InventoryMove(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    TIPO_CHOICES = [(IN, 'Entrada'), (OUT, 'Salida')]
    producto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movimientos')
    fecha = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=14, decimal_places=4)
    costo_unitario = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)  # requerido en ENTRADA
    referencia = models.CharField(max_length=120, blank=True, default='')

    class Meta:
        ordering = ['fecha', 'id']

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.tipo == self.IN and (self.costo_unitario is None):
            raise ValidationError("Las entradas requieren costo_unitario.")
        if self.tipo == self.OUT and self.costo_unitario is not None:
            # el costo de salidas se calcula por método, no se guarda aquí
            self.costo_unitario = None

    def __str__(self):
        return f"{self.fecha.date()} {self.tipo} {self.producto} {self.cantidad}"

# ======
# NÓMINA
# ======
class Employee(models.Model):
    activo = models.BooleanField(default=True)
    dui = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=120)
    salario_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField(default=timezone.now)
    def __str__(self):
        return f"{self.nombre} ({self.dui})"

class PayrollPeriod(models.Model):
    """Periodo mensual de planilla."""
    anio = models.PositiveIntegerField()
    mes = models.PositiveSmallIntegerField()  # 1-12
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anio', 'mes')
        ordering = ['-anio', '-mes']

    def __str__(self):
        return f"{self.anio}-{self.mes:02d}"

class PayrollLine(models.Model):
    periodo = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='lineas')
    empleado = models.ForeignKey(Employee, on_delete=models.PROTECT)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    isss = models.DecimalField(max_digits=10, decimal_places=2)
    afp = models.DecimalField(max_digits=10, decimal_places=2)
    renta = models.DecimalField(max_digits=10, decimal_places=2)
    otras_deducciones = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    liquido = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('periodo', 'empleado')

    def __str__(self):
        return f"{self.periodo} - {self.empleado} - {self.liquido}"
