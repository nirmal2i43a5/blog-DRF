
#Custom paginaiton
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )



class PostLimitOffsetPagination(LimitOffsetPagination):#using this shows ?offset=(pagenumber) i.e ?offset=2 --
    default_limit = 2  #data per page
    max_limit = 10


class PostPageNumberPagination(PageNumberPagination):#using this shows ?page=(pageno)  i.e ?page = 2 ---which is akin to my blog
    page_size = 2
    