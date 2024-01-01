from django.test import TestCase
from accounts.models import Profile, MyUser
from django.utils.text import slugify



from posts.models import Post


class PostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # create a user
        user=MyUser.objects.create_user(email="example@gmail.com", password="macy3663")
        user.save()
        # get the orofile needed for the post creation
        profile=MyUser.objects.get(email="example@gmail.com").user_profile

        # create post
        post1 = Post(
            profile=profile,
            title="This is a test post",
            bg_image="sample/image.jpg",
            cover_image="sample/image.jpg",
            slug=slugify("This is a test post"),
            summary="This is the sample summary",
            content="This is the sample summary",
        )
        post1.save()

        return super().setUpClass()
    
    def test_post_content(self):
        post=Post.objects.get(pk=1)
        profile=post.profile
        title=f"{post.title}"

        self.assertEqual(profile.user.email, "example@gmail.com")
        self.assertEqual(title, "This is a test post")
    
