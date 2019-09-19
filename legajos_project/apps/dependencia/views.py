from itertools import chain

from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from apps.cargo.models import Cargo
from apps.empleado.models import Empleado
from .models import DependenciaLaboral, Circunscripcion, Unidad, Organismo, Dependencia, Direccion, Departamento, \
    Division
from .forms import DependenciaLaboralForm


class DependenciaLaboralCreate(SuccessMessageMixin, CreateView):
    model = DependenciaLaboral
    form_class = DependenciaLaboralForm
    template_name = 'empleado/dependencia/dependencia_form.html'
    success_message = "¡La dependencia laboral fue agregada con éxito!"

    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('empleado_detail', args=[self.object.object_id])

    # def get_context_data(self, **kwargs):
    #     context = super(DependenciaLaboralCreate, self).get_context_data(**kwargs)
    #     id_empleado = self.kwargs.get('pk', 0)
    #     empleado = Empleado.objects.get(pk=id_empleado)
        # context['empleado'] = empleado
        # contenttype_obj = ContentType.objects.get_for_model(Empleado)
        # # Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo_anterior = None
        # try:
        #     cargo = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
        # except Cargo.DoesNotExist:
        #     cargo = None
        # context['cargo'] = cargo
        # # Intenta consultar la dependencia, si no tiene lanza la excepcion y pone cargo = None
        # try:
        #     dependencia = DependenciaLaboral.objects.get(object_id=empleado.id, content_type=contenttype_obj,
        #                                                  actual=True)
        # except DependenciaLaboral.DoesNotExist:
        #     dependencia = None
        # context['dependencia'] = dependencia
        # # Intenta consultar la dependencia, si no tiene lanza la excepcion y pone dependencia_anterior = None
        # try:
        #     dependencia_anterior = DependenciaLaboral.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
        # except DependenciaLaboral.DoesNotExist:
        #     dependencia_anterior = None
        # context['dependencia_anterior'] = dependencia_anterior
        # circunscripciones = Circunscripcion.objects.all()
        # unidades = Unidad.objects.all()
        # organismos = Organismo.objects.all()
        # dependencias = Dependencia.objects.all()
        # direcciones = Direccion.objects.all()
        # departamentos = Departamento.objects.all()
        # divisiones = Division.objects.all()
        # result_list = list(chain(circunscripciones, unidades, organismos, dependencias, direcciones, departamentos, divisiones))
        # context['listado_dependencias'] = result_list
        # context['titulo'] = "Agregar Dependencia Laboral"
        # context['DependenciaCreate'] = True
        # return context

    # def form_valid(self, form, **kwargs):
    #     user = self.request.user
    #     instance = form.save(commit=False)
    #     instance.created_by = user
    #     instance.modified_by = user
    #     id_empleado = self.kwargs.get('pk', 0)
    #     empleado = Empleado.objects.get(pk=id_empleado)
        # contenttype_obj = ContentType.objects.get_for_model(Empleado)
        # try:
        #     # Busco la dependencia anterior para ponerle actual = False, ya que la nueva dependencia será el actual
        #     dependencia_anterior = DependenciaLaboral.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
        #     dependencia_anterior.actual = False
        #     dependencia_anterior.save()
        # except DependenciaLaboral.DoesNotExist:
        #     dependencia = None
        # instance.object_id = empleado.id
        # instance.content_type = contenttype_obj
        # instance.save()
        # form.save_m2m()
        # return super().form_valid(form)


class DependenciaLaboralUpdate(SuccessMessageMixin, UpdateView):
    model = DependenciaLaboral
    form_class = DependenciaLaboralForm
    template_name = 'empleado/dependencia/dependencia_form.html'
    success_message = "¡La dependencia fue modificada con éxito!"

    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('empleado_detail', args=[self.object.object_id])

    # def get_context_data(self, **kwargs):
    #     context = super(DependenciaLaboralUpdate, self).get_context_data(**kwargs)
    #     id_empleado = self.kwargs.get('id_empleado', 0)
    #     empleado = Empleado.objects.get(pk=id_empleado)
        # contenttype_obj = ContentType.objects.get_for_model(Empleado)
        # # Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo_anterior = None
        # try:
        #     cargo = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
        # except Cargo.DoesNotExist:
        #     cargo = None
        # context['cargo'] = cargo
        # # Intenta consultar la dependencia, si no tiene lanza la excepcion y pone cargo = None
        # try:
        #     dependencia = DependenciaLaboral.objects.get(object_id=empleado.id, content_type=contenttype_obj,
        #                                                  actual=True)
        # except DependenciaLaboral.DoesNotExist:
        #     dependencia = None
        # context['dependencia'] = dependencia
        # circunscripciones = Circunscripcion.objects.all()
        # unidades = Unidad.objects.all()
        # organismos = Organismo.objects.all()
        # dependencias = Dependencia.objects.all()
        # direcciones = Direccion.objects.all()
        # departamentos = Departamento.objects.all()
        # divisiones = Division.objects.all()
        # result_list = list(chain(circunscripciones, unidades, organismos, dependencias, direcciones, departamentos, divisiones))
        # context['listado_dependencias'] = result_list
        # context['empleado'] = empleado
        # context['titulo'] = "Modificar Dependencia Laboral"
        # context['DependenciaUpdate'] = True
        # return context

    # def form_valid(self, form, **kwargs):
    #     user = self.request.user
    #     instance = form.save(commit=False)
    #     instance.created_by = user
    #     instance.modified_by = user
    #     id_empleado = self.kwargs.get('id_empleado', 0)
    #     empleado = Empleado.objects.get(pk=id_empleado)
        # contenttype_obj = ContentType.objects.get_for_model(Empleado)
        # try:
        #     # Busco la dependencia anterior para ponerle actual = False, ya que la nueva dependencia será la actual
        #     dependencia_anterior = DependenciaLaboral.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
        #     dependencia_anterior.actual = False
        #     dependencia_anterior.save()
        # except DependenciaLaboral.DoesNotExist:
        #     dependencia = None
        # instance.object_id = empleado.id
        # instance.content_type = contenttype_obj
        # instance.save()
        # form.save_m2m()
        # return super().form_valid(form)


class HistorialTraslados(DetailView):
    model = Empleado
    template_name = 'empleado/dependencia/historial_traslados.html'
    context_object_name = 'empleado'

    # def get_context_data(self, **kwargs):
    #     context = super(HistorialTraslados, self).get_context_data(**kwargs)

        # contenttype_obj = ContentType.objects.get_for_model(self.object)
        # # Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo_anterior = None
        # try:
        #     cargo = Cargo.objects.get(object_id=self.object.id, content_type=contenttype_obj, actual=True)
        # except Cargo.DoesNotExist:
        #     cargo = None
        # context['cargo'] = cargo
        # # Intenta consultar la dependencia, si no tiene lanza la excepcion y pone cargo = None
        # try:
        #     dependencia = DependenciaLaboral.objects.get(object_id=self.object.id, content_type=contenttype_obj,
        #                                                  actual=True)
        # except DependenciaLaboral.DoesNotExist:
        #     dependencia = None
        # context['dependencia'] = dependencia
        #
        # dependencias = DependenciaLaboral.objects.filter(object_id=self.object.id, content_type=contenttype_obj).order_by('-fecha_ingreso_dependencia')
        # context['dependencias'] = dependencias
        # context['HistorialTraslados'] = True
        # context['titulo'] = "Historial de Traslados"
        # return context
