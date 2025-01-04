# blog/permissions.py
from rest_framework.permissions import BasePermission
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any request (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Only allow write access if the user is the author of the post
        return obj.author == request.user


# List/Create view for posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Require authentication to create posts

    # Automatically assign the logged-in user as the author
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Retrieve/Update/Delete view for individual posts
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]  # Authenticated and owner-only access
