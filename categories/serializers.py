from rest_framework import serializers
from .models import Category


class CategorySerializerGet(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=255)
    parents = serializers.SerializerMethodField('get_parents')
    children = serializers.SerializerMethodField('get_children')
    siblings = serializers.SerializerMethodField('get_siblings')

    @staticmethod
    def get_parents(category):
        is_have_parent = False if not category.parent else True
        parent_list = []
        parent = {}
        if is_have_parent:
            parent = category.parent
        while is_have_parent:
            parent_object = {
                'id': parent.id,
                'name': parent.name
            }
            parent_list.append(parent_object)
            if parent.parent:
                parent = parent.parent
            else:
                is_have_parent = False
        return parent_list

    @staticmethod
    def get_children(category):
        children_list = []
        for child in Category.objects.filter(parent=category):
            child_object = {
                'id': child.id,
                'name': child.name
            }
            children_list.append(child_object)
        return children_list

    @staticmethod
    def get_siblings(category):
        siblings_list = []
        parent = None if not category.parent else category.parent
        if parent:
            for child in Category.objects.filter(parent=parent):
                if child != category:
                    child_object = {
                        'id': child.id,
                        'name': child.name
                    }
                    siblings_list.append(child_object)
        return siblings_list


class CategorySerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
