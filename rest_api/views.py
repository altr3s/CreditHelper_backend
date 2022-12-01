from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from os import getenv
import dotenv
from rest_framework.response import Response
from rest_api.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from braces.views import CsrfExemptMixin
from jwt.api_jwt import decode
import pandas as pd
from django.http import HttpResponse
import mimetypes

class RegisterView(generics.CreateAPIView, CsrfExemptMixin):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = []


class AddCreditView(generics.CreateAPIView):
    serializer_class = CreditSerializer
    authentication_classes = []
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        token = request.headers.get('Authorization').split()[1]
        dotenv.load_dotenv()
        decoded = decode(token, options={"verify_signature": True}, key=getenv('SECRET_KEY'), algorithms=[getenv('ALGORITHMS')])
        data.update({'user': decoded['id']})
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.data, status=403)
        

class GetCreditView(generics.CreateAPIView):

    def get(self, request):
        token = request.headers.get('Authorization').split()[1]
        dotenv.load_dotenv()
        decoded = decode(token, options={"verify_signature": True}, key=getenv('SECRET_KEY'), algorithms=[getenv('ALGORITHMS')])
        user_id = decoded['id']
        query = Credit.objects.filter(user=user_id)
        serializer = CreditSerializer(query, many=True)
        return Response(serializer.data)


class DownloadExcelView(generics.CreateAPIView):

    def get(self, request):
        token = request.headers.get('Authorization').split()[1]
        dotenv.load_dotenv()
        decoded = decode(token, options={"verify_signature": True}, key=getenv('SECRET_KEY'), algorithms=[getenv('ALGORITHMS')])
        user_id = decoded['id']
        query = Credit.objects.filter(user=user_id)
        array = CreditSerializer(query, many=True).data
        data = []
        columns = ['Сумма кредита', 'Ставка', 'Количество лет', 'Ежмес платеж', 'Общая сумма', 'Переплата']   
        for credit in array:
            data.append([credit['value'], credit['rate'], credit['years_count'], credit['monthly_payment'], credit['total_payment'], credit['overpay']])
        df = pd.DataFrame(data=data, columns=columns)
        df.index += 1 
        df.to_excel(excel_writer=f"downloads/{decoded['username']}_credits.xlsx", sheet_name='Кредиты')
        file_name = f"downloads/{decoded['username']}_credits.xlsx"
        file = open(file_name, 'rb')
        mime_type, _ = mimetypes.guess_type(file_name)
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % file_name
        return response
        

class DeleteCreditFromDB(generics.CreateAPIView):
    
    def post(self, request):
        data = request.data
        Credit.objects.filter(id=request.data['id']).delete()
        return Response({'Massage': 'success'})


class LoginAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.data, status=403)


@api_view(['GET'])
def health(request):
    return Response({'message': 'Backend server is online'})


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/add_credit/',
        '/api/my_credits',
        '/api/download',
        '/api/delete_credit'
    ]
    return Response(routes)
