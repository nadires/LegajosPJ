from itertools import chain

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from apps.empleado.models import Empleado
from .models import DependenciaLaboral, Circunscripcion, Unidad, Organismo, Dependencia, Direccion, Departamento, \
    Division
from .forms import DependenciaLaboralForm


class DependenciaLaboralCreate(SuccessMessageMixin, CreateView):
    model = DependenciaLaboral
    form_class = DependenciaLaboralForm
    template_name = 'empleado/dependencia/dependencia_form.html'
    success_message = "¡La dependencia laboral fue agregada con éxito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.empleado.id])

    def get_context_data(self, **kwargs):
        context = super(DependenciaLaboralCreate, self).get_context_data(**kwargs)
        id_empleado = self.kwargs.get('pk', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        context['empleado'] = empleado
        context['cargo'] = empleado.cargos_empleado.filter(actual=True).first()
        context['dependencia_anterior'] = empleado.dependencias_empleado.filter(actual=True).first()
        circunscripciones = Circunscripcion.objects.all()
        unidades = Unidad.objects.all()
        organismos = Organismo.objects.all()
        dependencias = Dependencia.objects.all()
        direcciones = Direccion.objects.all()
        departamentos = Departamento.objects.all()
        divisiones = Division.objects.all()
        result_list = list(chain(circunscripciones, unidades, organismos, dependencias, direcciones, departamentos, divisiones))
        context['listado_dependencias'] = result_list
        context['titulo'] = "Agregar Dependencia Laboral"
        context['DependenciaCreate'] = True
        return context

    def form_valid(self, form, **kwargs):
        user = self.request.user
        instance = form.save(commit=False)
        instance.created_by = user
        instance.modified_by = user
        id_empleado = self.kwargs.get('pk', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        DependenciaLaboral.objects.all().update(actual=False)
        instance.empleado = empleado
        instance.save()
        form.save_m2m()
        return super().form_valid(form)


class DependenciaLaboralUpdate(SuccessMessageMixin, UpdateView):
    model = DependenciaLaboral
    form_class = DependenciaLaboralForm
    template_name = 'empleado/dependencia/dependencia_form.html'
    success_message = "¡La dependencia fue modificada con éxito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.empleado.id])

    def get_context_data(self, **kwargs):
        context = super(DependenciaLaboralUpdate, self).get_context_data(**kwargs)
        id_empleado = self.kwargs.get('id_empleado', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        context['empleado'] = empleado
        context['cargo'] = empleado.cargos_empleado.filter(actual=True).first()
        context['dependencia'] = empleado.dependencias_empleado.filter(actual=True).first()
        circunscripciones = Circunscripcion.objects.all()
        unidades = Unidad.objects.all()
        organismos = Organismo.objects.all()
        dependencias = Dependencia.objects.all()
        direcciones = Direccion.objects.all()
        departamentos = Departamento.objects.all()
        divisiones = Division.objects.all()
        result_list = list(chain(circunscripciones, unidades, organismos, dependencias, direcciones, departamentos, divisiones))
        context['listado_dependencias'] = result_list
        context['titulo'] = "Modificar Dependencia Laboral"
        context['DependenciaUpdate'] = True
        return context

    def form_valid(self, form, **kwargs):
        user = self.request.user
        instance = form.save(commit=False)
        # instance.created_by = user
        instance.modified_by = user
        id_empleado = self.kwargs.get('id_empleado', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        instance.empleado = empleado
        instance.save()
        form.save_m2m()
        return super().form_valid(form)


class HistorialTraslados(DetailView):
    model = Empleado
    template_name = 'empleado/dependencia/historial_traslados.html'
    context_object_name = 'empleado'

    def get_context_data(self, **kwargs):
        context = super(HistorialTraslados, self).get_context_data(**kwargs)
        context['cargo'] = self.object.cargos_empleado.filter(actual=True).first()
        context['dependencia'] = self.object.dependencias_empleado.filter(actual=True).first()
        context['dependencias'] = self.object.dependencias_empleado.all().order_by('-fecha_ingreso_dependencia')
        context['HistorialTraslados'] = True
        context['titulo'] = "Historial de Traslados"
        return context
