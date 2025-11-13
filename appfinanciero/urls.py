# appfinanciero/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     # Productos
    path('productos/', views.product_list, name='product_list'),
    path('productos/nuevo/', views.product_create, name='product_create'),
    path('productos/<int:pk>/editar/', views.product_edit, name='product_edit'),
    path('productos/<int:pk>/eliminar/', views.product_delete, name='product_delete'),

    # Inventario
    path('movimientos/', views.move_list, name='move_list'),
    path('movimientos/nuevo/', views.move_create, name='move_create'),
    path('inventario/<int:producto_id>/<str:metodo>/', views.reporte_inventario, name='reporte_inventario'),

    # Empleados
    path('empleados/', views.employee_list, name='employee_list'),
    path('empleados/nuevo/', views.employee_create, name='employee_create'),
    path('empleados/<int:pk>/editar/', views.employee_edit, name='employee_edit'),
    path('empleados/<int:pk>/eliminar/', views.employee_delete, name='employee_delete'),

    # Parámetros & renta
    path('parametros/', views.payroll_config, name='payroll_config'),
    path('renta/', views.tax_list, name='tax_list'),
    path('renta/nuevo/', views.tax_create, name='tax_create'),
    path('renta/<int:pk>/eliminar/', views.tax_delete, name='tax_delete'),

    # Planilla
    path('planilla/<int:anio>/<int:mes>/', views.planilla_periodo, name='planilla_periodo'),
    path('planilla/<int:anio>/<int:mes>/excel/', views.planilla_excel, name='planilla_excel'),
    path('planilla/<int:anio>/<int:mes>/pdf/',   views.planilla_pdf,   name='planilla_pdf'),
    path('inventario/<int:producto_id>/<str:metodo>/excel/', views.inventario_excel, name='inventario_excel'),
    path('inventario/<int:producto_id>/<str:metodo>/pdf/',   views.inventario_pdf,   name='inventario_pdf'),

    path("productos/export/excel/", views.productos_excel, name="productos_excel"),
    path("productos/export/csv/",   views.productos_csv,   name="productos_csv"),
    path("productos/export/pdf/",   views.productos_pdf,   name="productos_pdf"),
    path("productos/importar/", views.importar_productos, name="importar_productos"),

    path("productos/", views.productos_list, name="productos_list"),
    path("productos/importar/", views.importar_productos, name="importar_productos"),
    path("productos/export/excel/", views.productos_excel, name="productos_excel"),
    path("productos/export/csv/", views.productos_csv, name="productos_csv"),
    path("productos/export/pdf/", views.productos_pdf, name="productos_pdf"),
    path("productos/plantilla/csv/", views.productos_plantilla_csv, name="productos_plantilla_csv"),

    path("integrantes/", views.integrantes, name="integrantes"),
]
