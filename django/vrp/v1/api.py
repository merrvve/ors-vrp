from ninja import Router
from .models import Vehicle, VehicleOut
from typing import List
router = Router()

@router.get("/vehicles", response=List[VehicleOut])
def list_vehicles(request):
    qs = Vehicle.objects.all()
    return qs
