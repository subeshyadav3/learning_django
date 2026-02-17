from django.shortcuts import render
from demo.models import Product
from demo.serializers import ProductSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def home(request):
    return render(request,'index.html')



class ProductList(APIView):
    def get(self,request):
        object = Product.objects.all()
        serializer = ProductSerializer(object,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'success','data':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
