# import all the needed models 
# for the listing of them in the sidebar
from posts.models import *
from shop.models import *


# now define the context dictionary for the listing of the models'

def get_administrator_context(request):
    return dict(
        post_post_model=Post,
    )