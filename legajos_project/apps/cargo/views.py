from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from apps.empleado.models import Empleado, DependenciaLaboral
from .models import Cargo
from .forms import CargoForm

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.contenttypes.models import ContentType

from datetime import datetime


class CargoCreate(SuccessMessageMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'empleado/cargo/cargo_form.html'
    success_message = "¡El cargo fue agregado con éxito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.object_id])

    def get_context_data(self, **kwargs):
        context = super(CargoCreate, self).get_context_data(**kwargs)
        id_empleado = self.kwargs.get('pk', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        context['empleado'] = empleado
        contenttype_obj = ContentType.objects.get_for_model(Empleado)
        # Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo_anterior = None
        try:
            cargo_anterior = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
        except Cargo.DoesNotExist:
            cargo_anterior = None
        # Intenta consultar la dependencia, si no tiene lanza la excepcion y pone cargo = None
        try:
            dependencia = DependenciaLaboral.objects.get(object_id=empleado.id, content_type=contenttype_obj,
                                                         actual=True)
        except DependenciaLaboral.DoesNotExist:
            dependencia = None
        context['dependencia'] = dependencia
        context['cargo'] = cargo_anterior
        context['titulo'] = "Agregar Cargo"
        context['CargoCreate'] = True
        return context

    def form_valid(self, form, **kwargs):
        user = self.request.user
        instance = form.save(commit=False)
        instance.created_by = user
        instance.modified_by = user
        id_empleado = self.kwargs.get('pk', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        contenttype_obj = ContentType.objects.get_for_model(Empleado)
        try:
            # Busco el cargo anterior para ponerle actual = False, ya que el nuevo cargo será el actual
            cargo_anterior = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
            cargo_anterior.actual = False
            if self.request.POST.get('fecha_fin_cargo_anterior'):
                cargo_anterior.fecha_fin_cargo = datetime.strptime(self.request.POST.get('fecha_fin_cargo_anterior'), "%d/%m/%Y")
            cargo_anterior.save()
        except Cargo.DoesNotExist:
            cargo = None
        instance.object_id = empleado.id
        instance.content_type = contenttype_obj
        instance.save()
        form.save_m2m()
        return super().form_valid(form)


class CargoUpdate(SuccessMessageMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'empleado/cargo/cargo_form.html'
    success_message = "¡El cargo fue modificado con éxito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.object_id])

    def get_context_data(self, **kwargs):
        context = super(CargoUpdate, self).get_context_data(**kwargs)
        id_empleado = self.kwargs.get('id_empleado', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        context['empleado'] = empleado
        contenttype_obj = ContentType.objects.get_for_model(Empleado)
        # Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo_anterior = None
        try:
            cargo = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
        except Cargo.DoesNotExist:
            cargo = None
        context['cargo'] = cargo
        # Intenta consultar la dependencia, si no tiene lanza la excepcion y pone cargo = None
        try:
            dependencia = DependenciaLaboral.objects.get(object_id=empleado.id, content_type=contenttype_obj,
                                                         actual=True)
        except DependenciaLaboral.DoesNotExist:
            dependencia = None
        context['dependencia'] = dependencia
        context['titulo'] = "Modificar Cargo"
        context['CargoUpdate'] = True
        return context

    def form_valid(self, form, **kwargs):
        user = self.request.user
        instance = form.save(commit=False)
        instance.created_by = user
        instance.modified_by = user
        id_empleado = self.kwargs.get('id_empleado', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        contenttype_obj = ContentType.objects.get_for_model(Empleado)
        try:
            # Busco el cargo anterior para ponerle actual = False, ya que el nuevo cargo será el actual
            cargo_anterior = Cargo.objects.get(object_id=empleado.id, content_type=contenttype_obj, actual=True)
            cargo_anterior.actual = False
            if self.request.POST.get('fecha_fin_cargo_anterior'):
                cargo_anterior.fecha_fin_cargo = datetime.strptime(self.request.POST.get('fecha_fin_cargo_anterior'), "%d/%m/%Y")
            cargo_anterior.save()
        except Cargo.DoesNotExist:
            cargo = None
        instance.object_id = empleado.id
        instance.content_type = contenttype_obj
        instance.save()
        form.save_m2m()
        return super().form_valid(form)


class FojaServicios(DetailView):
    model = Empleado
    template_name = 'empleado/cargo/foja_servicios.html'
    context_object_name = 'empleado'

    def get_context_data(self, **kwargs):
        context = super(FojaServicios, self).get_context_data(**kwargs)

        contenttype_obj = ContentType.objects.get_for_model(self.object)
        # Intenta consultar el cargo, si no tiene lanza la excepcion y pone cargo_anterior = None
        try:
            cargo = Cargo.objects.get(object_id=self.object.id, content_type=contenttype_obj, actual=True)
        except Cargo.DoesNotExist:
            cargo = None
        context['cargo'] = cargo
        # Intenta consultar la dependencia, si no tiene lanza la excepcion y pone cargo = None
        try:
            dependencia = DependenciaLaboral.objects.get(object_id=self.object.id, content_type=contenttype_obj,
                                                         actual=True)
        except DependenciaLaboral.DoesNotExist:
            dependencia = None
        context['dependencia'] = dependencia

        cargos = Cargo.objects.filter(object_id=self.object.id, content_type=contenttype_obj).order_by('-fecha_ingreso_cargo')
        context['cargos'] = cargos
        context['FojaServicios'] = True
        context['titulo'] = "Foja de Servicios"
        return context
