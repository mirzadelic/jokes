from rest_framework import routers
from views import *


router = routers.DefaultRouter()
router.register(r'joke', JokeViewSet)
router.register(r'category', CategoryViewSet)

api_urls = router.urls
