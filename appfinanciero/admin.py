# appfinanciero/admin.py
from django.contrib import admin
from .models import (
    Product, InventoryMove,
    Employee, PayrollPeriod, PayrollLine,
    PayrollConfig, TaxBracket
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'unidad')
    search_fields = ('codigo', 'nombre')

@admin.register(InventoryMove)
class InventoryMoveAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'producto', 'tipo', 'cantidad', 'costo_unitario', 'referencia')
    list_filter = ('tipo', 'producto')
    search_fields = ('referencia',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dui', 'salario_mensual', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'dui')

@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    list_display = ('anio', 'mes', 'fecha_creacion')
    ordering = ('-anio', '-mes')

@admin.register(PayrollLine)
class PayrollLineAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'empleado', 'salario_base', 'isss', 'afp', 'renta', 'liquido')
    list_filter = ('periodo',)

@admin.register(PayrollConfig)
class PayrollConfigAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'isss_empleado_pct', 'isss_techo', 'afp_empleado_pct')

@admin.register(TaxBracket)
class TaxBracketAdmin(admin.ModelAdmin):
    list_display = ('desde', 'hasta', 'cuota_fija', 'tasa_exceso_pct')
