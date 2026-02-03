from rest_framework import serializers
from .models import Blog, Comment


class CommentSerializer(serializers.ModelSerializer):
    # This serializer handles individual Comment objects.
    # It will automatically include all model fields because of fields="__all__".
    class Meta:
        model = Comment
        fields = "__all__"  # Serialize every field on the Comment model


class BlogSerializer(serializers.ModelSerializer):
    # Nested relationship: each Blog can include its related comments.
    # 'comments' here is the related_name on the Comment model's FK to Blog
    # (e.g. blog = models.ForeignKey(Blog, related_name="comments", ...)).
    #
    # many=True  -> A blog has multiple comments (one-to-many).
    # read_only=True -> Comments are only shown through BlogSerializer;
    #                   you cannot create/update comments via this nested field.
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        # '__all__' includes all Blog fields PLUS the nested 'comments' field above.
        # This means a blog response will look like:
        # {
        #   "id": 1,
        #   "title": "...",
        #   "content": "...",
        #   ... other Blog fields ...,
        #   "comments": [ { ...comment1... }, { ...comment2... } ]
        # }
        fields = '__all__'
