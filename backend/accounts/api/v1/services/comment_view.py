from posts.models import Post, BlogLike, BlogComment, CommentLike
from django.contrib.auth import get_user_model
User = get_user_model()


def get_blog_by_id(blog_id):
    return Post.objects.get(pk=blog_id)


def get_user_by_id(id):
    return User.objects.get(pk=id)



def create_comment(user, blog_item, blog_body, parent):
    blog_item = get_blog_by_id(blog_item)
    parent_obj = None
    if parent:
        try:
            parent_obj = BlogComment.objects.get(id=parent)
        except:
            pass

    return BlogComment.objects.create(
        blog_item=blog_item, user=user, blog_body=blog_body, parent=parent_obj
    )


def press_like_to_comment(request, comment_id):

    user = request.user
    comment = BlogComment.objects.get(id=comment_id)
    like = CommentLike.objects.filter(user=user, comment_blog_item=comment)

    if like:
        like.delete()  # thre is like put
    else:
        return CommentLike.objects.create(
            user=user, comment_blog_item=comment
        ).id  # create like
