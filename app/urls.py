from rest_framework import routers
from views import *


router = routers.DefaultRouter()
router.register(r'joke', JokeViewSet)

api_urls = router.urls
