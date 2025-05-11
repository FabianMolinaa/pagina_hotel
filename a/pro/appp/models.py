from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    CATEGORIA_OPCIONES = [
        ('AUTOMATICO', 'Automático'),
        ('MANUAL', 'Manual'),
    ]

    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion = models.TextField()
    stock = models.IntegerField()
    categoria = models.CharField(max_length=12, choices=CATEGORIA_OPCIONES)
    
    # Productos automáticos
    voltaje = models.IntegerField(null=True, blank=True)
    
    # Productos manuales
    material = models.CharField(max_length=50, null=True, blank=True)

    # Campo para la imagen del producto
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  # Almacena imágenes en el directorio 'productos/'

    def __str__(self):
        return self.nombre

class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Usuario: {self.usuario.username})"

class Compra(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('RECHAZADO', 'Rechazado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    orden_compra = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Compra {self.orden_compra} - {self.usuario.username}"
        
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de {self.compra.orden_compra} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)