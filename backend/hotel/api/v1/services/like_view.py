from posts.models import Post, BlogLike


def press_like_to_product(request, product_id,user_id):

    # user = request.user
    product = Post.objects.get(id=product_id)
    like = BlogLike.objects.filter(user=user_id, blog_item=product)

    new_like = ""
    if like:
        like.delete()  # thre is like put
    else:
        new_like = BlogLike.objects.create(user=user_id, blog_item=product)  # create like
    return new_like.id if new_like else None
