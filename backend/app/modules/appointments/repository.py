from datetime import date, time
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.appointments.models import (
    Appointment,
    AppointmentStatus,
)

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
        appointment_id: UUID,
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
        exclude_appointment_id: UUID | None = None,
) -> Appointment | None:

        query = db.query(Appointment).filter(
        Appointment.appointment_date == appointment_date,
        Appointment.status == AppointmentStatus.BOOKED,
        Appointment.start_time < end_time,
        Appointment.end_time > start_time,
    )

        if exclude_appointment_id:
            query = query.filter(
            Appointment.id != exclude_appointment_id
        )

        return query.first()
    
    from datetime import date

    def get_by_date(
    self,
    db: Session,
    appointment_date: date,
) -> list[Appointment]:
        return (
        db.query(Appointment)
        .filter(
            Appointment.appointment_date == appointment_date
        )
        .order_by(Appointment.start_time)
        .all()
    )
    
    def get_by_customer(
        self,
        db: Session,
        customer_id: UUID,
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