from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import Producto, CarritoItem
from .forms import ProductoForm
from django.contrib import messages 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from decimal import Decimal
import uuid
import datetime
from django.http import HttpResponse
from .bancoapi import dolar

def index(request):
    productos = Producto.objects.all()  
    return render(request, "index.html", {'productos': productos})

def catalogo(request):
    productos = Producto.objects.all()  
    return render(request, "catalogo.html", {'productos': productos})

@login_required
def crud(request):
    productos = []  

    query = request.GET.get('search', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    stock_min = request.GET.get('stock_min', '')
    product_id = request.GET.get('product_id', '')

    if query or precio_min or precio_max or stock_min or product_id:

        productos = Producto.objects.all()

        if query:
            productos = productos.filter(nombre__icontains=query)

        if precio_min:
            productos = productos.filter(precio__gte=precio_min)

        if precio_max:
            productos = productos.filter(precio__lte=precio_max)

        if stock_min:
            productos = productos.filter(stock__gte=stock_min)

        if product_id:
            productos = productos.filter(id=product_id)

    return render(request, 'crud.html', {
        'productos': productos,
        'query': query,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'stock_min': stock_min,
        'product_id': product_id,
    })
@login_required
def del_producto(request, product_id):
    try:
        producto = get_object_or_404(Producto, id=product_id)
        producto.delete()  

        productos = Producto.objects.all()
        context = {
            "mensaje": "Producto eliminado correctamente",  
            "productos": productos,
        }
        return redirect('crud')   

    except:
        productos = Producto.objects.all()  
        context = {
            "mensaje": "Error al eliminar el producto: ", 
            "productos": productos,
        }
        return render(request, "crud.html", context)

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('crud')  
    else:
        form = ProductoForm() 

    return render(request, 'agregar.html', {'form': form})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('crud')  # Redirige a la vista CRUD después de guardar
    return redirect('crud')

def salir(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

@login_required
def carrito(request):
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)  # Filtra los items por usuario
    else:
        carrito_items = []  # Si el usuario no está autenticado, el carrito está vacío

    total = sum(item.producto.precio * item.cantidad for item in carrito_items)  
    return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito_item, created = CarritoItem.objects.get_or_create(
        usuario=request.user,
        producto=producto
    )
    
    # Verificar si el stock es suficiente antes de agregar al carrito
    if carrito_item.cantidad < producto.stock:
        if not created:
            carrito_item.cantidad += 1
        carrito_item.save()
        messages.success(request, f'{producto.nombre} ha sido añadido al carrito.')
    else:
        messages.warning(request, f'No hay suficiente stock de {producto.nombre}.')
        
    return redirect('catalogo')

def update_carrito(request, product_id):
    if request.method == 'POST':
        change = int(request.POST.get('change', 0))  # Obtiene el cambio
        # Busca el item del carrito del usuario
        item = CarritoItem.objects.filter(usuario=request.user, producto__id=product_id).first()

        if item:
            # Verificar que la nueva cantidad no exceda el stock
            nueva_cantidad = item.cantidad + change
            if nueva_cantidad > item.producto.stock:
                messages.warning(request, f'Sólo hay {item.producto.stock} unidades disponibles de {item.producto.nombre}.')
            else:
                item.cantidad = nueva_cantidad  # Actualiza la cantidad
                if item.cantidad <= 0:
                    item.delete()  # Elimina el item si la cantidad es 0 o menor
                else:
                    item.save()  # Guarda los cambios si la cantidad es mayor a 0

        return redirect('carrito')  # Redirige a la vista del carrito

    return redirect('carrito')


# Configuración de credenciales de prueba
COMMERCE_CODE = "597055555532"
API_KEY = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

# Inicializar configuración
options = WebpayOptions(COMMERCE_CODE, API_KEY, IntegrationType.TEST)
tx = Transaction(options)


def generar_orden_compra():
    """Genera un número de orden de compra único y válido para Webpay"""
    fecha = datetime.datetime.now().strftime("%Y%m%d")
    unique = str(uuid.uuid4())[:5]
    return f"OC-{fecha}-{unique}"

def iniciar_pago(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        try:
            # Obtener los items del carrito del usuario
            carrito_items = CarritoItem.objects.filter(usuario=request.user)
            if not carrito_items.exists():
                return HttpResponse('Error: Carrito vacío', status=400)

        
            total = sum(item.producto.precio * item.cantidad for item in carrito_items)
            #amount = total / float(dolar)
            amount = int(total)
            buy_order = generar_orden_compra()
            session_id = str(request.user.id)  # Usar el ID del usuario como session_id
            return_url = request.build_absolute_uri('/respuesta/')
            
            print(f"Iniciando transacción: Order={buy_order}, Amount={amount}, User={request.user.username}")
            
            # Crear la transacción en Webpay
            response = tx.create(
                buy_order=buy_order,
                session_id=session_id,
                amount=amount,
                return_url=return_url
            )
            

            
            # Redireccionar al formulario de pago de Webpay
            url_webpay = response['url'] + "?token_ws=" + response['token']
            return redirect(url_webpay)
            
        except Exception as e:
            print(f"Error detallado: {str(e)}")
            return HttpResponse(f'Error al iniciar el pago: {str(e)}', status=500)
    
    return HttpResponse('Método no permitido', status=405)

@csrf_exempt
def respuesta(request):
    token = request.GET.get('token_ws')
    
    if not token:
        return render(request, 'respuesta.html', {
            'status': 'CANCELADO',
            'mensaje': 'Transacción cancelada por el usuario'
        })
    
    try:
        response = tx.commit(token)
        
        if response['status'] == 'AUTHORIZED':
            if request.user.is_authenticated:
                # Obtener items del carrito antes de eliminarlo
                carrito_items = CarritoItem.objects.filter(usuario=request.user)
                
                # Actualizar el stock de cada producto
                for item in carrito_items:
                    producto = item.producto
                    if producto.stock >= item.cantidad:
                        producto.stock -= item.cantidad
                        producto.save()
                    else:
                        # Si por alguna razón el stock es insuficiente, podrías
                        # registrar este error o manejarlo de otra manera
                        print(f"Error: Stock insuficiente para {producto.nombre}")
                
                # Vaciar el carrito después de actualizar el stock
                carrito_items.delete()
            
            context = {
                'status': 'EXITOSO',
                'mensaje': 'Pago realizado con éxito',
                'detalles': response
            }
            
            # Aquí podrías agregar código adicional para:
            # 1. Registrar la venta en una tabla de Ventas
            # 2. Enviar confirmación por email
            # 3. Generar factura/boleta
            
        else:
            context = {
                'status': 'RECHAZADO',
                'mensaje': f'Pago rechazado: {response["status"]}',
                'detalles': response
            }
            
    except Exception as e:
        context = {
            'status': 'ERROR',
            'mensaje': f'Error al procesar el pago: {str(e)}'
        }
    
    return render(request, 'respuesta.html', context)