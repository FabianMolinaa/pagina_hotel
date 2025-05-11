from django.urls import path
from appp import views
from .views import del_producto,agregar_producto,update_carrito

urlpatterns = [
    path("", views.index, name="index"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("crud/", views.crud, name="crud"),
    path("carrito/",views.carrito, name="carrito"),
    path('eliminar/<int:product_id>/', del_producto, name='del_producto'),
    path('agregar/', agregar_producto, name='agregar'),
    path('producto/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('salir/', views.salir, name='salir'),
    path('login/', views.login, name='conectar'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/update/<int:product_id>/', update_carrito, name='update_carrito'), 
    path('iniciar-pago/', views.iniciar_pago, name='iniciar_pago'),
    path('respuesta/', views.respuesta, name='respuesta'),

]