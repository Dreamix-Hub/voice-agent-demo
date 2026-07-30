from datetime import date, time, datetime
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.appointments.models import Appointment
from app.modules.appointments.models import (
    Appointment,
    AppointmentStatus,
)
from uuid import UUID
class AppointmentRepository:

    def create(
        self,
        db: Session,
        appointment: Appointment,
    ) -> Appointment:
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    def get_by_id(
        self,
        db: Session,
        appointment_id: uuid.UUID,
    ) -> Appointment | None:
        return (
            db.query(Appointment)
            .filter(Appointment.id == appointment_id)
            .first()
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Appointment]:
        return (
            db.query(Appointment)
            .order_by(
                Appointment.appointment_date,
                Appointment.start_time,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    def update(
        self,
        db: Session,
        appointment: Appointment,
    ) -> Appointment:
        db.commit()
        db.refresh(appointment)
        return appointment

    def delete(
        self,
        db: Session,
        appointment: Appointment,
    ) -> None:
        db.delete(appointment)
        db.commit()

    def find_conflict(
        self,
        db: Session,
        appointment_date: date,
        start_time: time,
        end_time: time,
        exclude_appointment_id: uuid.UUID | None = None,
    ) -> Appointment | None:

        query = db.query(Appointment).filter(
            Appointment.appointment_date == appointment_date,
            Appointment.status == AppointmentStatus.BOOKED,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time,
        )

        if exclude_appointment_id is not None:
            query = query.filter(
                Appointment.id != exclude_appointment_id
            )

        return query.first()

    def get_by_date(
        self,
        db: Session,
        appointment_date: date,
    ) -> list[Appointment]:
        return (
            db.query(Appointment)
            .filter(Appointment.appointment_date == appointment_date)
            .order_by(Appointment.start_time)
            .all()
        )

    def get_by_customer(
        self,
        db: Session,
        customer_id: uuid.UUID,
    ) -> list[Appointment]:
        return (
            db.query(Appointment)
            .filter(
                Appointment.customer_id == customer_id
            )
            .order_by(
                Appointment.appointment_date,
                Appointment.start_time,
            )
            .all()
        )

    def get_for_date(
    self,
    db: Session,
    *,
    target_date: date,
) -> list[Appointment]:
        statement = (
            select(Appointment)
            .where(
                Appointment.appointment_date == target_date,
            )
            .order_by(Appointment.start_time)
    )

        return list(db.scalars(statement).all())
    
    def get_customer_appointment_by_date(
    self,
    db: Session,
    *,
    customer_id: UUID,
    appointment_date: date,
) -> Appointment | None:
        return (
            db.query(Appointment)
            .filter(
                Appointment.customer_id == customer_id,
                Appointment.appointment_date == appointment_date,
                Appointment.status == AppointmentStatus.BOOKED,
            )
            .first()
    )
    
    def get_next_customer_appointment(
    self,
    db: Session,
    *,
    customer_id: UUID,
) -> Appointment | None:
        return (
            db.query(Appointment)
            .filter(
                Appointment.customer_id == customer_id,
                Appointment.status == AppointmentStatus.BOOKED,
                Appointment.appointment_date >= date.today(),
            )
            .order_by(
                Appointment.appointment_date.asc(),
                Appointment.start_time.asc(),
            )
            .first()
        )

