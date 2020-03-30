from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializerGet, CategorySerializerPost


def save_children(parent, children):
    child_object = {}
    for child in children:
        category = {
            'name': child['name'],
            'parent': parent.id
        }
        serializer = CategorySerializerPost(data=category)
        if serializer.is_valid(raise_exception=True):
            child_object = serializer.save()

        if child.get('children'):
            save_children(child_object, child['children'])


class CategoryView(APIView):
    def get(self, request, pk):
        try:
            categories = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializerGet(categories)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        parent = None
        children = request.data.get('children')
        child_object = {}
        category = {
            'name': name,
            'parent': parent
        }
        serializer = CategorySerializerPost(data=category)
        if serializer.is_valid(raise_exception=True):
            parent = serializer.save()

        for child in children:
            category = {
                'name': child['name'],
                'parent': parent.id
            }
            serializer = CategorySerializerPost(data=category)
            if serializer.is_valid(raise_exception=True):
                child_object = serializer.save()

            if child['children']:
                save_children(child_object, child['children'])
        return Response({'success': 'Categories saved'})
