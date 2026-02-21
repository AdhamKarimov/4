from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework.generics import GenericAPIView
from .models import Product
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ProductListCreateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        search = request.query_params.get('search')
        products = self.get_queryset()
        massage = 'Product'

        if search :
            q= Q(title__icontains=search) | Q(brand__icontains=search)
            mahsulot = products.filter(q)
            massage = 'Product'
            if mahsulot.exists():
                products = mahsulot
            else:
                massage = 'Product topilmadi'

        serializer = self.get_serializer(products, many=True)
        data = {
            'status': status.HTTP_200_OK,
            'message': massage,
            'products': serializer.data
        }
        return Response(data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': status.HTTP_201_CREATED,
                'massage': 'Product yaratildi',
                'products': serializer.data,
            }
            return Response(data)
        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'massage': 'XATO',
        }
        return Response(data)


class ProductUpdateDetailDeleteView(GenericAPIView):
    serializer_class = ProductSerializer

    def get_object(self,pk):
        product = Product.objects.filter(pk=pk).first()
        return product

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'status': status.HTTP_200_OK,
            'message': 'Product yangilandi',
            'product': serializer.data,
        }
        return Response(data)

    def patch(self,request,pk):
        product = self.get_object(pk)
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True,)
        serializer.save()
        data = {
            'status': status.HTTP_200_OK,
            'message': 'Product yangilandi',
            'product': serializer.data,
        }
        return Response(data)

    def get(self,request,pk):
        product = self.get_object(pk)
        serializer = self.get_serializer(product)
        data = {
            'status': status.HTTP_200_OK,
            'message': 'Product',
            'product': serializer.data,
        }
        return Response(data)

    def delete(self,request,pk):
        product = self.get_object(pk)
        if product is None:
            data = {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Product topilmadi',
            }
            return Response(data)
        product.delete()
        data = {
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Product ochirildi',
        }
        return Response(data)
