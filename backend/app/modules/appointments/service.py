from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.common.exceptions import (
    AppointmentConflictError,
    OutsideBusinessHoursError,
    AppointmentNotFoundError,
    BusinessInactiveError,
    AppointmentCompletedError
)
from app.common.utils.business import is_within_business_hours
from app.common.utils.datetime import calculate_end_time
from app.modules.appointments.models import (
    Appointment,
    AppointmentStatus,
)
from app.modules.appointments.repository import AppointmentRepository
from app.modules.appointments.schemas import (
    AppointmentCreate,
    AppointmentUpdate
)
from app.modules.business.service import BusinessService
from app.modules.customers.service import CustomerService

from datetime import date
class AppointmentService:

    def __init__(
        self,
        repository: AppointmentRepository,
        customer_service: CustomerService,
        business_service: BusinessService,
    ):
        self.repository = repository
        self.customer_service = customer_service
        self.business_service = business_service

    def create_appointment(
        self,
        db: Session,
        data: AppointmentCreate,
    ) -> Appointment:

        # 1. Verify customer exists
        customer = self.customer_service.get_customer(
            db,
            data.customer_id,
        )

        # 2. Load business settings
        business = self.business_service.get_business(db)

        # 3. Check if business is active
        if not business.is_active:
            raise BusinessInactiveError()

        # 4. Calculate appointment end time
        end_time = calculate_end_time(
            start_time=data.start_time,
            duration_minutes=business.appointment_duration,
            buffer_minutes=business.buffer_time,
        )

        # 5. Validate business hours
        if not is_within_business_hours(
            start_time=data.start_time,
            end_time=end_time,
            opening_time=business.opening_time,
            closing_time=business.closing_time,
        ):
            raise OutsideBusinessHoursError()

        # 6. Check for conflicting appointment
        conflict = self.repository.find_conflict(
            db=db,
            appointment_date=data.appointment_date,
            start_time=data.start_time,
            end_time=end_time,
        )

        if conflict:
            raise AppointmentConflictError()

        # 7. Create appointment
        appointment = Appointment(
            customer_id=customer.id,
            appointment_date=data.appointment_date,
            start_time=data.start_time,
            end_time=end_time,
            status=AppointmentStatus.BOOKED,
            reason=data.reason,
            notes=data.notes,
        )

        return self.repository.create(
            db,
            appointment,
        )
        
    def get_all_appointments(
        self,
        db: Session,
    ):
        return self.repository.get_all(db)   
    
    def get_appointment(
        self,
        db: Session,
        appointment_id: UUID,
):
        appointment = self.repository.get_by_id(
        db,
        appointment_id,
    )

        if not appointment:
            raise AppointmentNotFoundError()

        return appointment
    def update_appointment(
    self,
    db: Session,
    appointment_id: UUID,
    data: AppointmentUpdate,
    ) -> Appointment:

        appointment = self.get_appointment(db, appointment_id)

        if appointment.status != AppointmentStatus.BOOKED:
            raise AppointmentCompletedError()

        business = self.business_service.get_business(db)

        appointment_date = (
            data.appointment_date
            if data.appointment_date is not None
            else appointment.appointment_date
    )

        start_time = (
            data.start_time
            if data.start_time is not None
            else appointment.start_time
    )

        end_time = calculate_end_time(
            start_time=start_time,
            duration_minutes=business.appointment_duration,
            buffer_minutes=business.buffer_time,
    )

        if not is_within_business_hours(
            start_time=start_time,
            end_time=end_time,
            opening_time=business.opening_time,
            closing_time=business.closing_time,
    ):
            raise OutsideBusinessHoursError()

        conflict = self.repository.find_conflict(
            db=db,
            exclude_appointment_id=appointment.id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
    )

        if conflict:
            raise AppointmentConflictError()

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(appointment, field, value)

        appointment.end_time = end_time

        return self.repository.update(db, appointment)
    
    def update_status(
    self,
    db: Session,
    appointment_id: UUID,
    status: AppointmentStatus,
) -> Appointment:

        appointment = self.get_appointment(
        db,
        appointment_id,
    )

        if appointment.status != AppointmentStatus.BOOKED:
            raise AppointmentCompletedError()

        appointment.status = status

        return self.repository.update(
        db,
        appointment,
    )
        
    def cancel_appointment(
    self,
    db: Session,
    appointment_id: UUID,
) -> Appointment:

        appointment = self.get_appointment(
        db,
        appointment_id,
    )

        if appointment.status != AppointmentStatus.BOOKED:
            raise AppointmentCompletedError()

        appointment.status = AppointmentStatus.CANCELLED

        return self.repository.update(
        db,
        appointment,
    )
   
    def get_appointments_by_date(
    self,
    db: Session,
    appointment_date: date,
):
        return self.repository.get_by_date(
        db,
        appointment_date,
    )
    
    def get_customer_appointments(
    self,
    db: Session,
    customer_id: UUID,
):
    # Verify the customer exists
        self.customer_service.get_customer(
        db,
        customer_id,
    )

        return self.repository.get_by_customer(
        db,
        customer_id,
    )