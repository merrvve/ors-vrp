from ninja import NinjaAPI
from v1.api import router as v1_router

api = NinjaAPI()

api.add_router("/v1/", v1_router)    # You can add router object

