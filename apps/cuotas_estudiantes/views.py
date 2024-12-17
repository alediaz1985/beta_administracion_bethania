from django.shortcuts import render, get_object_or_404, redirect
from .models import Preinscripcion, Inscripcion, Cuota
from apps.administracion_alumnos.models import Estudiante
from django.utils.timezone import now

# Vista para listar cuotas
from django.shortcuts import render
from .models import Cuota


def listar_cuotas(request):
    cuotas = Cuota.objects.select_related('estudiante', 'mes').prefetch_related('mes__ciclo_lectivo')
    return render(request, 'cuotas_estudiantes/listar_cuotas.html', {'cuotas': cuotas})


def registrar_cuota(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)

    if request.method == "POST":
        mes = request.POST.get("mes")
        monto = float(request.POST.get("monto"))
        fecha_pago = request.POST.get("fecha_pago")  # Ejemplo: 2024-03-15

        cuota = Cuota.objects.create(
            estudiante=estudiante,
            mes=mes,
            monto=monto,
            fecha_pago=fecha_pago,
            pagada=True
        )
        return redirect('listar_cuotas')

    return render(request, 'cuotas_estudiantes/registrar_cuota.html', {'estudiante': estudiante})


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import CicloLectivo, Inscripcion, Cuota
from apps.administracion_alumnos.models import Estudiante


def listar_ciclos(request):
    ciclos = CicloLectivo.objects.all().order_by('anio')
    return render(request, 'cuotas_estudiantes/listar_ciclos.html', {'ciclos': ciclos})

# Vista para registrar una inscripción
def registrar_inscripcion(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    if request.method == "POST":
        ciclo_id = request.POST.get('ciclo_lectivo')
        ciclo = get_object_or_404(CicloLectivo, id=ciclo_id)
        monto = request.POST.get('monto_inscripcion')
        Inscripcion.objects.create(estudiante=estudiante, ciclo_lectivo=ciclo, monto_inscripcion=monto, pagada=False)
        return redirect(reverse('listar_inscripciones'))
    ciclos = CicloLectivo.objects.all()
    return render(request, 'cuotas_estudiantes/registrar_inscripcion.html', {'estudiante': estudiante, 'ciclos': ciclos})

# Vista para listar inscripciones
def listar_inscripciones(request):
    inscripciones = Inscripcion.objects.select_related('estudiante', 'ciclo_lectivo').all()
    return render(request, 'cuotas_estudiantes/listar_inscripciones.html', {'inscripciones': inscripciones})

# Vista para registrar el pago de una cuota
def registrar_pago_cuota(request, cuota_id):
    cuota = get_object_or_404(Cuota, id=cuota_id)
    if request.method == "POST":
        cuota.fecha_pago = request.POST.get('fecha_pago')
        cuota.pagada = True
        cuota.save()
        return redirect(reverse('listar_cuotas'))
    return render(request, 'cuotas_estudiantes/registrar_pago.html', {'cuota': cuota})



from django.shortcuts import render, redirect
from .forms import CicloLectivoForm

def registrar_ciclo_lectivo(request):
    if request.method == "POST":
        form = CicloLectivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cuotas_estudiantes:listar_ciclos')  # Redirige a la lista de ciclos
    else:
        form = CicloLectivoForm()
    return render(request, 'cuotas_estudiantes/registrar_ciclo_lectivo.html', {'form': form})



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import CicloLectivo

def habilitar_ciclo(request, ciclo_id):
    ciclo = get_object_or_404(CicloLectivo, id=ciclo_id)
    if ciclo.habilitado:
        messages.warning(request, f"El ciclo {ciclo.anio} ya está habilitado.")
    else:
        ciclo.habilitado = True
        ciclo.save()
        messages.success(request, f"El ciclo {ciclo.anio} ha sido habilitado correctamente.")
    return redirect('cuotas_estudiantes:listar_ciclos')


from django.shortcuts import render, redirect
from .models import MontosCicloLectivo, CicloLectivo, NivelEducativo
from .forms import MontosCicloLectivoForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import MontosCicloLectivo, CicloLectivo, NivelEducativo
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import MontosCicloLectivo, CicloLectivo, NivelEducativo
from django.utils import timezone




def registrar_montos(request):
    if request.method == 'POST':
        ciclo_id = request.POST.get('ciclo_lectivo')
        nivel_id = request.POST.get('nivel_educativo')
        monto_inscripcion = request.POST.get('monto_inscripcion')
        monto_cuota = request.POST.get('monto_cuota')
        descuento = request.POST.get('descuento_anticipado')

        ciclo_lectivo = CicloLectivo.objects.get(id=ciclo_id)
        nivel_educativo = NivelEducativo.objects.get(id=nivel_id)

        # Desactivar montos anteriores
        MontosCicloLectivo.objects.filter(
            ciclo_lectivo=ciclo_lectivo, 
            nivel_educativo=nivel_educativo, 
            activo=True
        ).update(activo=False)

        # Crear un nuevo registro activo
        MontosCicloLectivo.objects.create(
            ciclo_lectivo=ciclo_lectivo,
            nivel_educativo=nivel_educativo,
            monto_inscripcion=monto_inscripcion,
            monto_cuota=monto_cuota,
            descuento_anticipado=descuento,
            fecha_creacion=timezone.now(),
            activo=True
        )

        # Redirigir usando el namespace 'cuotas_estudiantes:listar_montos'
        return redirect('cuotas_estudiantes:listar_montos')

    ciclos = CicloLectivo.objects.all()
    niveles = NivelEducativo.objects.all()
    return render(request, 'cuotas_estudiantes/registrar_montos.html', {
        'ciclos': ciclos,
        'niveles': niveles
    })

from django.shortcuts import render
from .models import MontosCicloLectivo

def listar_montos(request):
    filtro_estado = request.GET.get('estado', 'todos')
    if filtro_estado == 'activos':
        montos = MontosCicloLectivo.objects.filter(activo=True)
    elif filtro_estado == 'inactivos':
        montos = MontosCicloLectivo.objects.filter(activo=False)
    else:
        montos = MontosCicloLectivo.objects.all()

    return render(request, 'cuotas_estudiantes/listar_montos.html', {
        'montos': montos,
        'filtro_estado': filtro_estado,
    })


from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import MontosCicloLectivo

def cambiar_estado_monto(request, monto_id):
    monto = get_object_or_404(MontosCicloLectivo, id=monto_id)

    if not monto.activo:
        # Desactivar otros montos activos del mismo ciclo lectivo y nivel educativo
        MontosCicloLectivo.objects.filter(
            ciclo_lectivo=monto.ciclo_lectivo,
            nivel_educativo=monto.nivel_educativo,
            activo=True
        ).update(activo=False)
    
    # Cambiar el estado del monto seleccionado
    monto.activo = not monto.activo
    monto.save()

    return redirect('cuotas_estudiantes:listar_montos')


from django.shortcuts import render, get_object_or_404
from .models import Inscripcion, Cuota, CicloLectivo
from apps.administracion_alumnos.models import Estudiante

def estado_deuda_por_ciclo(request, estudiante_id):
    # Obtener el estudiante
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    
    # Obtener ciclo lectivo seleccionado desde el formulario GET
    ciclo_lectivo_id = request.GET.get("ciclo_lectivo")
    ciclo_lectivo = None
    inscripcion = None
    cuotas = []

    if ciclo_lectivo_id:
        # Obtener el ciclo lectivo seleccionado
        ciclo_lectivo = get_object_or_404(CicloLectivo, id=ciclo_lectivo_id)

        # Obtener la inscripción del estudiante en el ciclo lectivo seleccionado
        inscripcion = Inscripcion.objects.filter(
            estudiante=estudiante,
            ciclo_lectivo=ciclo_lectivo
        ).first()

        # Obtener las cuotas asociadas al ciclo lectivo
        if inscripcion:
            cuotas = Cuota.objects.filter(
                estudiante=estudiante,
                mes__ciclo_lectivo=ciclo_lectivo
            ).order_by('mes__nombre')

    # Obtener todos los ciclos lectivos disponibles
    ciclos = CicloLectivo.objects.all()

    return render(request, 'cuotas_estudiantes/estado_deuda.html', {
        'estudiante': estudiante,
        'inscripcion': inscripcion,
        'cuotas': cuotas,
        'ciclo_lectivo': ciclo_lectivo,
        'ciclos': ciclos
    })

from django.shortcuts import render, get_object_or_404
from .models import CicloLectivo, Inscripcion, Cuota, MesCicloLectivo
from apps.administracion_alumnos.models import Estudiante
from django.db.models import F, Q, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce

from django.shortcuts import render, get_object_or_404
from .models import Inscripcion, CicloLectivo, Cuota
from datetime import date

from decimal import Decimal  # Importa Decimal para realizar cálculos
from decimal import Decimal
from datetime import date

def listado_estado_deuda(request):
    ciclo_lectivo_id = request.GET.get("ciclo_lectivo")
    ciclo_lectivo = None
    inscripciones = []

    if ciclo_lectivo_id:
        ciclo_lectivo = get_object_or_404(CicloLectivo, id=ciclo_lectivo_id)
        inscripciones = Inscripcion.objects.filter(ciclo_lectivo=ciclo_lectivo).select_related('estudiante')

        for inscripcion in inscripciones:
            cuotas = Cuota.objects.filter(
                estudiante=inscripcion.estudiante,
                mes__ciclo_lectivo=ciclo_lectivo
            ).select_related('mes').order_by('mes__nombre')

            for cuota in cuotas:
                hoy = date.today()
                mes_cuota = cuota.mes.nombre  # Nombre del mes de la cuota
                anio_cuota = ciclo_lectivo.anio  # Año del ciclo lectivo
                fecha_limite_pago = date(anio_cuota, obtener_numero_mes(mes_cuota), 10)  # Día 10 del mes

                # Verificar si la cuota está fuera de término y no pagada
                if not cuota.pagada:
                    if hoy > fecha_limite_pago and hoy.year >= fecha_limite_pago.year:
                        # Solo aplica si la fecha actual supera la fecha límite y estamos en el mismo año o posterior
                        cuota.interes_por_mora = Decimal("10.0")  # 10% de interés por mora
                        cuota.total_a_pagar = cuota.monto_base + (cuota.monto_base * cuota.interes_por_mora / Decimal("100"))
                    else:
                        cuota.interes_por_mora = Decimal("0.0")
                        cuota.total_a_pagar = cuota.monto_base
                else:
                    # Si la cuota ya está pagada
                    cuota.interes_por_mora = Decimal("0.0")
                    cuota.total_a_pagar = cuota.monto_base

            inscripcion.cuotas = cuotas

    ciclos_lectivos = CicloLectivo.objects.all()
    return render(request, "cuotas_estudiantes/listado_estado_deuda.html", {
        "ciclos_lectivos": ciclos_lectivos,
        "ciclo_lectivo": ciclo_lectivo,
        "inscripciones": inscripciones
    })

# Helper para convertir el nombre del mes a número
def obtener_numero_mes(nombre_mes):
    meses = {
        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
        "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
        "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }
    return meses.get(nombre_mes, 0)


from django.shortcuts import render, redirect
from .models import NivelEducativo
from django.http import HttpResponse

def registrar_nivel_educativo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            NivelEducativo.objects.get_or_create(nombre=nombre)
            return redirect('cuotas_estudiantes:listar_niveles')
        else:
            return HttpResponse("El nombre del nivel educativo no puede estar vacío.", status=400)
    return render(request, 'cuotas_estudiantes/registrar_nivel.html')


def listar_niveles(request):
    niveles = NivelEducativo.objects.all()
    return render(request, 'cuotas_estudiantes/listar_niveles.html', {'niveles': niveles})


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from apps.administracion_alumnos.models import Estudiante
from .models import Preinscripcion, NivelEducativo

from django.db.models import Max

from django.shortcuts import render, redirect
from .models import Preinscripcion, Estudiante, NivelEducativo, CicloLectivo


from django.shortcuts import render
from .models import Preinscripcion

def listar_preinscripciones(request):
    # Optimiza la consulta con select_related para evitar múltiples consultas a la base de datos.
    preinscripciones = Preinscripcion.objects.select_related('estudiante', 'nivel_educativo').all()
    return render(request, 'cuotas_estudiantes/listar_preinscripciones.html', {
        'preinscripciones': preinscripciones
    })

from datetime import datetime 
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from apps.administracion_alumnos.models import Estudiante
from apps.cuotas_estudiantes.models import Preinscripcion, NivelEducativo

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from apps.administracion_alumnos.models import Estudiante
from .models import Preinscripcion, NivelEducativo

from django.db.models import Max

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Preinscripcion, NivelEducativo
from apps.administracion_alumnos.models import Estudiante

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Preinscripcion, NivelEducativo
from apps.administracion_alumnos.models import Estudiante
from django.utils.timezone import now

from django.db.models import Max
from django.db import models
from django.shortcuts import render, redirect
from .models import Preinscripcion, Estudiante, NivelEducativo, CicloLectivo

from django.db import models  # Importación necesaria
from django.shortcuts import render, redirect
from .models import Preinscripcion, Estudiante, NivelEducativo, CicloLectivo

from django.db import models
from django.shortcuts import render, redirect
from .models import Preinscripcion, Estudiante, NivelEducativo, CicloLectivo
from django.db import models
from django.shortcuts import render, redirect
from .models import Preinscripcion, Estudiante, NivelEducativo, CicloLectivo

def registrar_preinscripcion(request):
    ciclo_lectivo_id = request.GET.get("ciclo_lectivo")  # Obtiene el ciclo lectivo seleccionado
    ciclo_lectivo_seleccionado = None

    if ciclo_lectivo_id:
        ciclo_lectivo_seleccionado = CicloLectivo.objects.get(id=ciclo_lectivo_id)

    # Obtener estudiantes más recientes por CUIL (última marca temporal)
    estudiantes_mas_recientes = Estudiante.objects.filter(
        id__in=Estudiante.objects.values('cuil_estudiante').annotate(
            max_id=models.Max('id')  # Obtener el último registro basado en el ID
        ).values('max_id')
    )

    # Filtrar estudiantes que no están preinscriptos en el ciclo lectivo seleccionado
    if ciclo_lectivo_seleccionado:
        estudiantes = estudiantes_mas_recientes.exclude(
            preinscripciones__ciclo_lectivo=ciclo_lectivo_seleccionado
        )
    else:
        estudiantes = estudiantes_mas_recientes

    # Datos para el formulario
    niveles = NivelEducativo.objects.all()
    ciclos_lectivos = CicloLectivo.objects.all()

    if request.method == "POST":
        estudiante_id = request.POST.get("estudiante")
        nivel_id = request.POST.get("nivel_educativo")

        estudiante = Estudiante.objects.get(id=estudiante_id)
        nivel = NivelEducativo.objects.get(id=nivel_id)

        # Validar duplicado para el ciclo lectivo
        if Preinscripcion.objects.filter(estudiante=estudiante, ciclo_lectivo=ciclo_lectivo_seleccionado).exists():
            return render(request, "cuotas_estudiantes/registrar_preinscripcion.html", {
                "niveles": niveles,
                "ciclos_lectivos": ciclos_lectivos,
                "estudiantes": estudiantes,
                "error": "El estudiante ya está preinscripto en este ciclo lectivo."
            })

        # Crear preinscripción
        Preinscripcion.objects.create(
            estudiante=estudiante,
            nivel_educativo=nivel,
            ciclo_lectivo=ciclo_lectivo_seleccionado
        )
        return redirect("cuotas_estudiantes:listar_preinscripciones")

    return render(request, "cuotas_estudiantes/registrar_preinscripcion.html", {
        "niveles": niveles,
        "ciclos_lectivos": ciclos_lectivos,
        "estudiantes": estudiantes,
        "ciclo_lectivo_seleccionado": ciclo_lectivo_seleccionado
    })


from django.shortcuts import render
from .models import Preinscripcion, Inscripcion

from .models import Preinscripcion, CicloLectivo

def listar_preinscripciones_para_inscripcion(request):
    ciclo_lectivo_id = request.GET.get("ciclo_lectivo")
    ciclo_lectivo_seleccionado = None
    preinscripciones = []

    if ciclo_lectivo_id:
        ciclo_lectivo_seleccionado = CicloLectivo.objects.get(id=ciclo_lectivo_id)
        # Filtrar preinscripciones que no tienen una inscripción asociada en el ciclo seleccionado
        preinscripciones = Preinscripcion.objects.filter(
            ciclo_lectivo=ciclo_lectivo_seleccionado
        ).exclude(
            estudiante__inscripcion__ciclo_lectivo=ciclo_lectivo_seleccionado
        ).select_related('estudiante', 'nivel_educativo')

    ciclos = CicloLectivo.objects.all()
    return render(request, 'cuotas_estudiantes/listar_preinscripciones_inscripcion.html', {
        'ciclos': ciclos,
        'preinscripciones': preinscripciones,
        'ciclo_lectivo_seleccionado': ciclo_lectivo_seleccionado
    })


from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.urls import reverse
from .models import Preinscripcion, Inscripcion, Cuota, MesCicloLectivo

@transaction.atomic
def inscribir_estudiante(request, preinscripcion_id):
    # Obtener la preinscripción
    preinscripcion = get_object_or_404(Preinscripcion, id=preinscripcion_id)

    # Verificar si el estudiante ya tiene una inscripción
    if Inscripcion.objects.filter(estudiante=preinscripcion.estudiante).exists():
        return render(request, 'cuotas_estudiantes/error.html', {
            'mensaje': 'El estudiante ya está inscrito en un ciclo lectivo.'
        })

    # Crear la inscripción
    inscripcion = Inscripcion.objects.create(
        estudiante=preinscripcion.estudiante,
        ciclo_lectivo=preinscripcion.ciclo_lectivo,
        monto_inscripcion=10000,  # Ajusta la lógica del monto
        pagada=False
    )

    # Generar cuotas para los meses del ciclo lectivo
    meses = MesCicloLectivo.objects.filter(ciclo_lectivo=preinscripcion.ciclo_lectivo)
    for mes in meses:
        Cuota.objects.create(
            estudiante=preinscripcion.estudiante,
            mes=mes,
            monto_base=8000,  # Ajusta el monto según tu lógica
            pagada=False
        )

    # Redirigir al listado de preinscripciones
    return redirect(reverse('cuotas_estudiantes:listar_preinscripciones_para_inscripcion'))


"""

from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from .models import Preinscripcion, Inscripcion, Cuota, MesCicloLectivo, CicloLectivo
from django.urls import reverse

@transaction.atomic
def inscribir_estudiante(request, preinscripcion_id):
    preinscripcion = get_object_or_404(Preinscripcion, id=preinscripcion_id)

    # Verificar si ya está inscrito en el ciclo lectivo
    if Inscripcion.objects.filter(
        estudiante=preinscripcion.estudiante, ciclo_lectivo=preinscripcion.ciclo_lectivo
    ).exists():
        return render(request, 'cuotas_estudiante/error.html', {'mensaje': 'El estudiante ya está inscrito en este ciclo.'})

    # Crear la inscripción
    inscripcion = Inscripcion.objects.create(
        estudiante=preinscripcion.estudiante,
        ciclo_lectivo=preinscripcion.ciclo_lectivo,
        monto_inscripcion=10000,  # Monto fijo o dinámico según tu lógica
        pagada=False
    )

    # Generar cuotas para los meses del ciclo lectivo
    meses = MesCicloLectivo.objects.filter(ciclo_lectivo=preinscripcion.ciclo_lectivo)
    for mes in meses:
        Cuota.objects.create(
            estudiante=preinscripcion.estudiante,
            mes=mes,
            monto_base=8000,  # Ajustar monto según tu lógica
            pagada=False
        )

    return redirect(reverse('cuotas_estudiantes:listar_preinscripciones_para_inscripcion'))



from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from .models import Preinscripcion, Inscripcion, Cuota, MesCicloLectivo, CicloLectivo

@transaction.atomic
def inscribir_estudiante(request, preinscripcion_id):
    # Obtener la preinscripción
    preinscripcion = get_object_or_404(Preinscripcion, id=preinscripcion_id)

    # Verificar si ya está inscrito
    if Inscripcion.objects.filter(estudiante=preinscripcion.estudiante).exists():
        return render(request, 'cuotas_estudiante/error.html', {'mensaje': 'El estudiante ya está inscrito.'})

    # Obtener el ciclo lectivo habilitado
    ciclo_lectivo = CicloLectivo.objects.filter(habilitado=True).latest('fecha_inicio')

    # Crear la inscripción
    inscripcion = Inscripcion.objects.create(
        estudiante=preinscripcion.estudiante,
        ciclo_lectivo=ciclo_lectivo,
        monto_inscripcion=10000,  # Cambiar según lógica
        pagada=False
    )

    # Crear cuotas para los meses del ciclo lectivo
    meses = MesCicloLectivo.objects.filter(ciclo_lectivo=ciclo_lectivo)
    for mes in meses:
        Cuota.objects.create(
            estudiante=preinscripcion.estudiante,
            mes=mes,
            monto_base=8000,  # Cambiar según lógica
            pagada=False
        )

    # Redirigir al listado de inscripciones
    return redirect('cuotas_estudiantes:listar_preinscripciones_para_inscripcion')"""

from django.shortcuts import render
from .models import Inscripcion

from django.shortcuts import render
from .models import Inscripcion, CicloLectivo

def listar_inscripciones(request):
    ciclo_lectivo_id = request.GET.get('ciclo_lectivo')  # Obtener el ciclo lectivo desde el formulario
    ciclos = CicloLectivo.objects.all().order_by('anio')  # Obtener todos los ciclos lectivos

    # Filtrar inscripciones según el ciclo lectivo seleccionado
    if ciclo_lectivo_id:
        inscripciones = Inscripcion.objects.filter(ciclo_lectivo_id=ciclo_lectivo_id).select_related('estudiante', 'ciclo_lectivo')
    else:
        inscripciones = Inscripcion.objects.select_related('estudiante', 'ciclo_lectivo').all()

    return render(request, 'cuotas_estudiantes/listar_inscripciones.html', {
        'inscripciones': inscripciones,
        'ciclos': ciclos,
        'ciclo_lectivo_id': ciclo_lectivo_id  # Pasar la selección actual al template
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Inscripcion
from apps.administracion_alumnos.models import Estudiante
from django.db.models import Max
from django.contrib import messages
from django.urls import reverse

def pagar_inscripcion(request):
    if request.method == "POST":
        cuil = request.POST.get("cuil")
        
        # Obtener el estudiante más reciente con el CUIL
        estudiante = Estudiante.objects.filter(
            cuil_estudiante=cuil
        ).order_by('-marca_temporal').first()
        
        if not estudiante:
            messages.error(request, "No se encontró un estudiante con ese CUIL.")
            return redirect('cuotas_estudiantes:pagar_inscripcion')

        # Obtener la inscripción pendiente de pago
        inscripcion = Inscripcion.objects.filter(
            estudiante=estudiante, pagada=False
        ).first()

        if not inscripcion:
            messages.error(request, "No hay inscripción pendiente de pago para este alumno.")
            return redirect('cuotas_estudiantes:pagar_inscripcion')

        # Marcar la inscripción como pagada
        inscripcion.pagada = True
        inscripcion.fecha_inscripcion = now()  # Fecha actual
        inscripcion.save()

        messages.success(request, f"Pago registrado correctamente para {estudiante.nombres_estudiante}.")
        return redirect('cuotas_estudiantes:listar_inscripciones')

    return render(request, "cuotas_estudiantes/pagar_inscripcion.html")

from django.shortcuts import render, get_object_or_404, redirect
from .models import Cuota
from apps.administracion_alumnos.models import Estudiante
from django.utils.timezone import now
from django.db.models import F
from django.contrib import messages

def pagar_cuotas(request):
    cuotas_adeudadas = []
    estudiante = None

    if request.method == "POST":
        # Obtener el CUIL del formulario
        cuil = request.POST.get("cuil")
        
        # Buscar el estudiante con la última marca temporal
        estudiante = Estudiante.objects.filter(
            cuil_estudiante=cuil
        ).order_by('-marca_temporal').first()
        
        if not estudiante:
            messages.error(request, "No se encontró un estudiante con ese CUIL.")
        else:
            # Buscar las cuotas adeudadas del estudiante
            cuotas_adeudadas = Cuota.objects.filter(
                estudiante=estudiante, pagada=False
            ).select_related('mes')

        # Procesar el pago de las cuotas seleccionadas
        if "pagar_cuotas" in request.POST:
            cuotas_seleccionadas = request.POST.getlist("cuotas")
            for cuota_id in cuotas_seleccionadas:
                cuota = Cuota.objects.get(id=cuota_id)
                cuota.pagada = True
                cuota.fecha_pago = now()
                cuota.save()
            messages.success(request, "Pago de cuotas registrado correctamente.")
            return redirect('cuotas_estudiantes:pagar_cuotas')

    return render(request, "cuotas_estudiantes/pagar_cuotas.html", {
        "estudiante": estudiante,
        "cuotas_adeudadas": cuotas_adeudadas
    })

from django.urls import get_resolver, reverse
from django.shortcuts import render

def panel_administracion(request):
    urls = []
    resolver = get_resolver()  # Resolver principal de Django
    app_namespace = "cuotas_estudiantes"

    # Acceder a las URLs del namespace actual
    for url in resolver.url_patterns:
        if hasattr(url, "namespace") and url.namespace == app_namespace:
            for sub_url in url.url_patterns:
                if hasattr(sub_url, 'name') and sub_url.name:  # Filtrar rutas con nombre
                    try:
                        # Detectar parámetros opcionales y asignar valores de ejemplo
                        kwargs = {}
                        if 'estudiante_id' in str(sub_url.pattern):
                            kwargs['estudiante_id'] = 1
                        if 'cuota_id' in str(sub_url.pattern):
                            kwargs['cuota_id'] = 1
                        if 'ciclo_id' in str(sub_url.pattern):
                            kwargs['ciclo_id'] = 1
                        if 'preinscripcion_id' in str(sub_url.pattern):
                            kwargs['preinscripcion_id'] = 1
                        
                        url_final = reverse(f"{app_namespace}:{sub_url.name}", kwargs=kwargs)
                        urls.append({
                            "name": sub_url.name.replace('_', ' ').title(),
                            "url": url_final
                        })
                    except Exception as e:
                        print(f"Error al procesar {sub_url.name}: {e}")

    return render(request, 'cuotas_estudiantes/panel_administracion.html', {'urls': urls})
