import random
import string
from twilio.rest import Client
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser

# Twilio credentials


account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_number = settings.TWILIO_NUMBER
client = Client(account_sid, auth_token)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp(phone_number, otp):
    message = client.messages.create(
        body=f'Your OTP for login into LoConnect is: {otp}',
        from_=twilio_number,
        to=phone_number
    )

class SendOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')#usecountrycode
        otp = generate_otp()
       
        user_profile, created = UserProfile.objects.get_or_create(phone_number=phone_number)
        user_profile.otp=otp
        user_profile.save()

        serializer = UserProfileSerializer(user_profile)
     
        send_otp(phone_number, otp)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        entered_otp = request.data.get('otp')
        try:
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            stored_otp = str(user_profile.otp).strip()
            entered_otp = str(entered_otp).strip() 
            print(stored_otp,entered_otp)

            if stored_otp == entered_otp:

                user_profile.otp = None
                user_profile.save()
                refresh = RefreshToken.for_user(user_profile)
                access_token = str(refresh.access_token)
                
                serializer = UserProfileSerializer(user_profile)
                return Response({'token': access_token, 'user': serializer.data}, status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        
class CategoryView(APIView):
    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   



class ServiceView(APIView):
    def post(self,request):
        serializer = ServiceSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceImageView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = ServiceImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
