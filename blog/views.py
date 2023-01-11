from .models import *
from .serializers import * 
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate


def get_tokens(user):   #creating tokens manually 
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
#register 
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'error': False,
                    'data': serializer.data,
                    'message': 'User has successfully been created.',
                    'status': status.HTTP_201_CREATED
                },
                status=status.HTTP_201_CREATED)

        return Response(
            {
                'error': True,
                'message': serializer.errors,
                'status': status.HTTP_400_BAD_REQUEST
            },
            status=status.HTTP_400_BAD_REQUEST)
#Post user 
class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        try:
            if 'id' in request.data:
                id = request.data['id']
                obj = Post.objects.get(id=id)
                serializer = Post(obj, many=False).data 
            else:
                obj = Post.objects.all()
                serializer = PostSerializer(obj, many=True).data 
            return Response(
                {'error':False, 
                 'data': serializer}, 
                status=status.HTTP_200_OK)
        except :
            return Response({
                'error':True,
                'data': "id is required "}, status=status.HTTP_400_BAD_REQUEST)  
            
    def post(self,request):
        try:
            title = request.data['title']
            content = request.data['content']
            Post.objects.create(
                title = title,
                author = request.user,
                content = content
            )
            return Response({'error':False, 'data':'post was successfully'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error':True, 'data':'Error unable to post'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def patch(self,request):
        try:
            id = request.data['id']
            obj = Post.objects.get(id= id)
        except:
            return Response({'error':True,'data':"id is required",},status=status.HTTP_400_BAD_REQUEST)
        try:
            title = request.data['title']
            obj.title = title
        except:
            pass   
        try:
            content = request.data['content']
            obj.content = content
        except:
            pass
        obj.save()
        return Response({
                'error':False, 
                'data':'post successfully Updated.',
                "status" : status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
    
    # def patch(self,request):
    #     try:
    #         id = request.data['id']
    #         obj = Post.objects.get(id=id)
    #         serializer = PostUpdateSerializer(obj,data=request.data,partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'error':False, 'data':'News post successfully edit'}, status=status.HTTP_202_ACCEPTED)
    #         return Response({'error':True,'data':'Unsucess news edit'},status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'error':True,'data':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
        
        
    def delete(self,request):
        try:
            id = request.data['id']
            obj = Post.objects.get(id=id)
            obj.delete()
            return Response({
                'error':False, 
                'data':'News post successfully delete.',
                "status" : status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except:
            return Response({
                'error':True,
                'data': "id required",
                'status': status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)

#lOGIN api 
class LoginAPI(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
        except:
            return Response({
                'error' : True,
                'data' : "enter email and pasword",
                "status" : status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user = authenticate(email=email, password=password, request=request)
        print(user)
        if user is None:
            response = {
                'error' : True,
                'data' : "Invalid email and password",
                "status" : status.HTTP_401_UNAUTHORIZED,
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            jwt_access_token = get_tokens(user)
            response = {
                    'status_code': status.HTTP_200_OK,
                    'data': 'Logged in successfully.',
                    'access_token': jwt_access_token["access"],
                    'refresh_token': jwt_access_token["refresh"],}
            return Response(response, status=status.HTTP_200_OK)
    
