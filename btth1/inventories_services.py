from fastapi import Request
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from database import SessionLocal
from models import ParkingSlot


class ParkingSlotCreate(BaseModel):
    slot_code: str 
    zone_name: str 
    max_weight: int 
    is_available: bool = True


def response_format(statusCode, message, error, data, path):
    return {
        "statusCode": statusCode,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def create_slot(slot: ParkingSlotCreate, request: Request):

    db = SessionLocal()

    try:

        exist = db.query(ParkingSlot).filter(
            ParkingSlot.slot_code == slot.slot_code
        ).first()

        if exist:
            return response_format(
                400,
                "Slot code already exists",
                "Bad Request",
                None,
                request.url.path
            )

        new_slot = ParkingSlot(
            slot_code=slot.slot_code,
            zone_name=slot.zone_name,
            max_weight=slot.max_weight,
            is_available=slot.is_available
        )

        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return response_format(
            201,
            "Thêm vị trí đỗ xe thành công",
            None,
            {
                "id": new_slot.id,
                "slot_code": new_slot.slot_code,
                "zone_name": new_slot.zone_name,
                "max_weight": new_slot.max_weight,
                "is_available": new_slot.is_available
            },
            request.url.path
        )

    except SQLAlchemyError:

        db.rollback()

        return response_format(
            500,
            "Database Error",
            "Internal Server Error",
            None,
            request.url.path
        )

    finally:
        db.close()


def get_all_slots(request: Request):

    db = SessionLocal()

    try:

        slots = db.query(ParkingSlot).all()

        data = []

        for slot in slots:
            data.append({
                "id": slot.id,
                "slot_code": slot.slot_code,
                "zone_name": slot.zone_name,
                "max_weight": slot.max_weight,
                "is_available": slot.is_available
            })

        return response_format(
            200,
            "Lấy danh sách vị trí đỗ xe thành công",
            None,
            data,
            request.url.path
        )

    except SQLAlchemyError:

        return response_format(
            500,
            "Database Error",
            "Internal Server Error",
            None,
            request.url.path
        )

    finally:
        db.close()


def get_slot(slot_id: int, request: Request):

    db = SessionLocal()

    try:

        slot = db.query(ParkingSlot).filter(
            ParkingSlot.id == slot_id
        ).first()

        if not slot:

            return response_format(
                404,
                "Parking slot not found",
                "Not Found",
                None,
                request.url.path
            )

        return response_format(
            200,
            "Lấy thông tin vị trí đỗ xe thành công",
            None,
            {
                "id": slot.id,
                "slot_code": slot.slot_code,
                "zone_name": slot.zone_name,
                "max_weight": slot.max_weight,
                "is_available": slot.is_available
            },
            request.url.path
        )

    except SQLAlchemyError:

        return response_format(
            500,
            "Database Error",
            "Internal Server Error",
            None,
            request.url.path
        )

    finally:
        db.close()