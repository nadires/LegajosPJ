from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from apps.empleado.models import Empleado
from .models import Cargo
from .forms import CargoForm

from django.contrib.messages.views import SuccessMessageMixin

from datetime import datetime


class CargoCreate(SuccessMessageMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'empleado/cargo/cargo_form.html'
    success_message = "¡El cargo fue agregado con éxito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.empleado.id])

    def get_context_data(self, **kwargs):
        context = super(CargoCreate, self).get_context_data(**kwargs)
        id_empleado = self.kwargs.get('pk', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        context['empleado'] = empleado
        cargo = empleado.cargos_empleado.filter(actual=True).first()
        context['cargo_anterior'] = cargo
        context['cargo'] = cargo
        context['dependencia'] = empleado.dependencias_empleado.filter(actual=True).first()
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
        cargo_anterior = empleado.cargos_empleado.filter(actual=True).first()
        cargo_anterior.actual = False
        if 'fecha_fin_cargo_anterior' in form.cleaned_data:
            cargo_anterior.fecha_fin_cargo = form.cleaned_data['fecha_fin_cargo_anterior']
        cargo_anterior.save()
        instance.empleado = empleado
        instance.save()
        form.save_m2m()
        return super().form_valid(form)


class CargoUpdate(SuccessMessageMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'empleado/cargo/cargo_form.html'
    success_message = "¡El cargo fue modificado con éxito!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('empleado_detail', args=[self.object.empleado.id])

    def get_context_data(self, **kwargs):
        context = super(CargoUpdate, self).get_context_data(**kwargs)
        id_empleado = self.kwargs.get('id_empleado', 0)
        empleado = Empleado.objects.get(pk=id_empleado)
        context['empleado'] = empleado
        context['cargo'] = empleado.cargos_empleado.filter(actual=True).first()
        context['dependencia'] = empleado.dependencias_empleado.filter(actual=True).first()
        context['titulo'] = "Modificar Cargo"
        context['CargoUpdate'] = True
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


class FojaServicios(DetailView):
    model = Empleado
    template_name = 'empleado/cargo/foja_servicios.html'
    context_object_name = 'empleado'

    def get_context_data(self, **kwargs):
        context = super(FojaServicios, self).get_context_data(**kwargs)
        context['cargo'] = self.object.cargos_empleado.filter(actual=True).first()
        context['dependencia'] = self.object.dependencias_empleado.filter(actual=True).first()
        context['cargos'] = self.object.cargos_empleado.all().order_by('-fecha_ingreso_cargo')
        context['FojaServicios'] = True
        context['titulo'] = "Foja de Servicios"
        return context
