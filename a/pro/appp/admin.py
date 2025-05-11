from django.contrib import admin

# Register your models here.
from .models import Producto,CarritoItem,Compra, DetalleCompra


admin.site.register(Producto)
admin.site.register(CarritoItem)
admin.site.register(Compra)
admin.site.register(DetalleCompra)