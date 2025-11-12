# appfinanciero/services.py
from decimal import Decimal
from .models import InventoryMove, PayrollConfig, TaxBracket, PayrollLine, PayrollPeriod, Employee

# ---------------------------
# INVENTARIO: FIFO / LIFO
# ---------------------------
def valuacion_inventario(producto, metodo='FIFO'):
    """Retorna (existencias, costo_total, costo_promedio) y lista de capas."""
    entradas = list(
        InventoryMove.objects.filter(producto=producto, tipo=InventoryMove.IN).order_by('fecha', 'id')
        .values('cantidad', 'costo_unitario')
    )
    salidas = list(
        InventoryMove.objects.filter(producto=producto, tipo=InventoryMove.OUT).order_by('fecha', 'id')
        .values('cantidad')
    )

    # ‘capas’ de inventario: lista de dicts con cantidad y costo
    capas = []
    for e in entradas:
        capas.append({'qty': Decimal(e['cantidad']), 'cost': Decimal(e['costo_unitario'])})

    if metodo.upper() == 'LIFO':
        capas = list(capas)  # ya están en orden; para LIFO usaremos pop() del final

    # aplicar salidas
    for s in salidas:
        qty = Decimal(s['cantidad'])
        while qty > 0 and capas:
            idx = -1 if metodo.upper() == 'LIFO' else 0
            capa = capas[idx]
            tomar = min(qty, capa['qty'])
            capa['qty'] -= tomar
            qty -= tomar
            if capa['qty'] == 0:
                capas.pop(idx)
        if qty > 0:
            # salidas mayores a existencias -> queda negativo (no recomendado)
            raise ValueError("No hay existencias suficientes para cubrir una salida.")

    existencia = sum(c['qty'] for c in capas)
    costo_total = sum(c['qty'] * c['cost'] for c in capas)
    costo_promedio = (costo_total / existencia) if existencia > 0 else Decimal('0.00')
    return existencia, costo_total, costo_promedio, capas

# ---------------------------
# NÓMINA
# ---------------------------
def _get_config():
    cfg = PayrollConfig.objects.first()
    if not cfg:
        cfg = PayrollConfig.objects.create()
    return cfg

def calcular_renta_mensual(base_gravable: Decimal) -> Decimal:
    """Usa los tramos guardados en TaxBracket. Si no hay, no descuenta renta."""
    tramo = None
    for t in TaxBracket.objects.order_by('desde'):
        if t.hasta is None:
            if base_gravable >= t.desde:
                tramo = t
        else:
            if t.desde <= base_gravable <= t.hasta:
                tramo = t
        if tramo:
            break
    if not tramo:
        return Decimal('0.00')
    exceso = base_gravable - tramo.desde
    if exceso < 0:
        exceso = Decimal('0.00')
    return tramo.cuota_fija + (exceso * (tasa := (tramo.tasa_exceso_pct / Decimal('100'))))

def generar_planilla(periodo: PayrollPeriod):
    """Genera/actualiza líneas de planilla para todos los empleados activos."""
    cfg = _get_config()
    for emp in Employee.objects.filter(activo=True):
        salario = emp.salario_mensual

        isss_base = min(salario, cfg.isss_techo)
        isss = (isss_base * cfg.isss_empleado_pct) / Decimal('100')

        afp = (salario * cfg.afp_empleado_pct) / Decimal('100')

        base_gravable = salario - isss - afp
        renta = calcular_renta_mensual(base_gravable)

        liquido = salario - isss - afp - renta

        line, _ = PayrollLine.objects.update_or_create(
            periodo=periodo, empleado=emp,
            defaults=dict(
                salario_base=salario,
                isss=isss.quantize(Decimal('0.01')),
                afp=afp.quantize(Decimal('0.01')),
                renta=renta.quantize(Decimal('0.01')),
                liquido=liquido.quantize(Decimal('0.01')),
            )
        )
    return periodo.lineas.all()
