from fastapi import FastAPI, Request
from inventories_services import (
    ParkingSlotCreate,
    create_slot,
    get_all_slots,
    get_slot
)
app = FastAPI()
@app.post("/parking-slots", status_code=201)
def add_parking_slot(slot: ParkingSlotCreate, request: Request):
    return create_slot(slot, request)


@app.get("/parking-slots")
def read_all_slots(request: Request):
    return get_all_slots(request)


@app.get("/parking-slots/{slot_id}")
def read_slot(slot_id: int, request: Request):
    return get_slot(slot_id, request)