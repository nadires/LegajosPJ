from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from rest_framework.response import Response
from django.http import Http404

from .serializers import EmpleadoSerializer
from ..models import Empleado, Circunscripcion, Unidad, Organismo, Dependencia, Direccion, Departamento, Division
from rest_framework import filters


class EmpleadoModelViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer


class EmpleadoApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        elements = Empleado.objects.all()
        serializer = EmpleadoSerializer(elements, many=True)
        response_dict = {
            'code': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'Success'
        }
        return JsonResponse(response_dict)



class EmpleadoViewSet(viewsets.ViewSet):
    # permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return Empleado.objects.get(pk=pk)
        except Empleado.DoesNotExist:
            raise Http404

    def list(self, request):
        queryset = Empleado.objects.all()
        serializer = EmpleadoSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = EmpleadoSerializer(instance)
        return Response(serializer.data)


class EmpleadoViewSetReadOnly(viewsets.ReadOnlyModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('apellido', 'nombre', 'legajo')


class EndpointDependencias(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        if 'tipo' in request.data and 'cod' in request.data:
            if request.data['tipo'] == 'Circunscripción':
                res = Circunscripcion.objects.get(pk=request.data['cod'])
                data = {
                    'id_circunscripcion': res.pk,
                    'id_unidad': "",
                    'id_organismo': "",
                    'id_dependencia': "",
                    'id_direccion': "",
                    'id_departamento': "",
                    'id_division': "",
                }
            elif request.data['tipo'] == 'Unidad':
                res = Unidad.objects.get(pk=request.data['cod'])
                data = {
                    'id_circunscripcion': res.circunscripcion.pk,
                    'id_unidad': res.pk,
                    'id_organismo': "",
                    'id_dependencia': "",
                    'id_direccion': "",
                    'id_departamento': "",
                    'id_division': "",
                }
            elif request.data['tipo'] == 'Organismo':
                res = Organismo.objects.get(pk=request.data['cod'])
                data = {
                    'id_circunscripcion': res.unidad.circunscripcion.pk,
                    'id_unidad': res.unidad.pk,
                    'id_organismo': res.pk,
                    'id_dependencia': "",
                    'id_direccion': "",
                    'id_departamento': "",
                    'id_division': "",
                }
            elif request.data['tipo'] == 'Dependencia':
                res = Dependencia.objects.get(pk=request.data['cod'])
                data = {
                    'id_circunscripcion': res.organismo.unidad.circunscripcion.pk,
                    'id_unidad': res.organismo.unidad.pk,
                    'id_organismo': res.organismo.pk,
                    'id_dependencia': res.pk,
                    'id_direccion': "",
                    'id_departamento': "",
                    'id_division': "",
                }
            elif request.data['tipo'] == 'Dirección':
                res = Direccion.objects.get(pk=request.data['cod'])
                data = {
                    'id_circunscripcion': res.dependencia.organismo.unidad.circunscripcion.pk,
                    'id_unidad': res.dependencia.organismo.unidad.pk,
                    'id_organismo': res.dependencia.organismo.pk,
                    'id_dependencia': res.dependencia.pk,
                    'id_direccion': res.pk,
                    'id_departamento': "",
                    'id_division': "",
                }
            elif request.data['tipo'] == 'Departamento':
                res = Departamento.objects.get(pk=request.data['cod'])
                data = {
                    'id_circunscripcion': res.direccion.dependencia.organismo.unidad.circunscripcion.pk,
                    'id_unidad': res.direccion.dependencia.organismo.unidad.pk,
                    'id_organismo': res.direccion.dependencia.organismo.pk,
                    'id_dependencia': res.direccion.dependencia.pk,
                    'id_direccion': res.direccion.pk,
                    'id_departamento': res.pk,
                    'id_division': "",
                }
            elif request.data['tipo'] == 'División':
                res = Division.objects.get(pk=request.data['cod'])
                data = {
                    'id_circunscripcion': res.departamento.direccion.dependencia.organismo.unidad.circunscripcion.pk,
                    'id_unidad': res.departamento.direccion.dependencia.organismo.unidad.pk,
                    'id_organismo': res.departamento.direccion.dependencia.organismo.pk,
                    'id_dependencia': res.departamento.direccion.dependencia.pk,
                    'id_direccion': res.departamento.direccion.pk,
                    'id_departamento': res.departamento.pk,
                    'id_division': res.pk,
                }
            else:
                return Response({'message': 'Error en parámetros'}, status.HTTP_400_BAD_REQUEST)
            response_dict = {
                'code': status.HTTP_200_OK,
                'data': data,
                'message': 'Success'
            }
            return Response(response_dict, status.HTTP_200_OK)
        else:
            return Response({'message': 'Error'}, status.HTTP_400_BAD_REQUEST)