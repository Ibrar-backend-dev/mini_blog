
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Q

from .permissions import IsPostAuthorOrReadOnly
from .models import Post
from.serializers import PostSerializer

class PostViewSet(ModelViewSet):
    
    # filter posts by author id
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Post.objects.filter(
                Q(is_private = False)|Q(author=user)
                ).order_by('-created_at')
        
        return Post.objects.filter(
            is_private = False
            ).order_by('-created_at')

    def perform_create(self, serializer):

        serializer.save(author = self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)
        return Response(
            {"message": "your message is deleted"},
            status=status.HTTP_200_OK,
        )
    
class PostViewSetv2(APIView):

    def get(self , request):                      
        posts = Post.objects.all()              #get all posts 
       
        visible_posts=[]                        # empty list 

        for post in posts:                      # loop through posts

            if not post.is_private :                  #public posts 
                visible_posts.append(post)

            elif request.user.is_authenticated:               # Own private post  
                if post.author_id == request.user.id:
                    visible_posts.append(post)

        serializer = PostSerializer(visible_posts, many = True)         #serialize list

        return Response(serializer.data , status=status.HTTP_200_OK)


    def post(self , request):
        if not request.user.is_authenticated :              # check logged in user
            return Response(
               {"message" : "User is not logged in." }, status=status.HTTP_401_UNAUTHORIZED
            )
       
        

        serializer = PostSerializer(data = request.data)            # put data in serializer

        if serializer.is_valid():           # validate serializer

            serializer.save(author=request.user)        # save post with user as author 

            return Response(
                serializer.data , status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors , status=status.HTTP_400_BAD_REQUEST
        )


class PostDetailViewSetv2(APIView):
     
    def get(self , request , pk):

        try:
            post = Post.objects.get(pk=pk)           # find post by id
        except Post.DoesNotExist:
            return Response(
                {"message":f"Post with post id {pk} does not exists."} , status=status.HTTP_404_NOT_FOUND
            )
        
        if post.is_private:             #check if post is private or not 

            if request.user != post.author:                #check requested user is author 
                return Response(
                    {"message":"You do not have permission to see this post."}, status=status.HTTP_403_FORBIDDEN
                )
            
        serializer= PostSerializer(post)            #serialize post

        return Response(
            serializer.data ,status=status.HTTP_200_OK
        )
            

    def put(self , request , pk ):
                                                    
        if not request.user.is_authenticated :        # check logged in user
            return Response(
               {"message" : "User is not logged in." }, status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            post = Post.objects.get(pk=pk)           # find post by id

        except Post.DoesNotExist:
            return Response(
                {"message":"Does not exists."} , status=status.HTTP_404_NOT_FOUND
            )
        
        if request.user != post.author:                #check requested user is author 
            return Response(
                    {"message":"You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN
                )
        
        serializer= PostSerializer(post , data =request.data)      # old and new data for update

        if serializer.is_valid():               # serializer validation 

            serializer.save()               # save updated data
            return Response(
                serializer.data , status=status.HTTP_200_OK
            )
        return Response(
                serializer.errors , status= status.HTTP_400_BAD_REQUEST
        )
    
    def patch(self , request , pk):

        if not request.user.is_authenticated :        # check logged in user
            return Response(
               {"message" : "User is not logged in." }, status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            post = Post.objects.get(pk=pk)           # find post by id

        except Post.DoesNotExist:
            return Response(
                {"message":"Does not exists."} , status=status.HTTP_404_NOT_FOUND
            )
        
        if request.user != post.author:                #check requested user is author 
            return Response(
                    {"message":"You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN
                )
        
        serializer= PostSerializer(post , data =request.data , partial=True)      # old and new data for update

        if serializer.is_valid():               # serializer validation 

            serializer.save()               # save updated data
            return Response(
                serializer.data , status=status.HTTP_200_OK
            )
        return Response(
                serializer.errors , status= status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self , request , pk):

        if not request.user.is_authenticated :        # check logged in user
            return Response(
               {"message" : "User is not logged in." }, status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            post = Post.objects.get(pk=pk)           # find post by id

        except Post.DoesNotExist:
            return Response(
                {"message":"Does not exists."} , status=status.HTTP_404_NOT_FOUND
            )
        
        if request.user != post.author:                #check ownership of post 
            return Response(
                    {"message":"You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN
                )
        
        post.delete()                   # delete the post

        return Response(
            {"message":"Your post is deleted successfully."}, status=status.HTTP_200_OK
        )
    
