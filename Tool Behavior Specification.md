Tool Behavior Specification (TBS)

Project: AI Receptionist

Version: 1.0

## Check Availability
Purpose

Retrieve all available appointment slots for a requested date.

Customer Intent

The customer wants to know when appointments are available.

Examples:

I'd like to make an appointment.

Are you available tomorrow?

What times do you have on Friday?

Required Information
Field	Required
Appointment Date	✅
Optional Information
Field	Required
Preferred Time	Optional
Preconditions

The AI must know:

appointment date

The AI should not ask for the reason for the visit before checking availability unless the business requires it.

When to Call

Examples

Customer:

Do you have anything tomorrow?

↓

Call

check_availability()

Customer

What times are available on July 28?

↓

Call

check_availability()
When NOT to Call

Don't call if:

No appointment date has been provided.
The customer is still deciding on a date.
The customer is asking about something unrelated.
Success Response

Present the available slots naturally.

Example:

I have openings at 10 AM, 1 PM, and 3 PM. Which one works best for you?

Failure Response

Example:

I'm sorry, I couldn't check the schedule right now. Could we try again in a moment?

## Book Appointment
Purpose

Create a confirmed appointment.

Customer Intent

The customer wants to reserve an available appointment.

Required Information
Field	Required
Date	✅
Time	✅

(Reason is optional unless the business requires it.)

Preconditions

Before calling this tool:

✔ Customer selected a date.

✔ Customer selected a time.

✔ Customer explicitly confirmed.

Never Call If

The customer says:

Let me think.

↓

Don't book.

Customer

What else do you have?

↓

Don't book.

Customer

Maybe.

↓

Don't book.

Success Response

Perfect! I've booked your appointment for Tuesday at 10 AM.

Failure Response

I'm sorry, it looks like that time is no longer available. Let's choose another time.

## Cancel Appointment
Purpose

Cancel an existing booked appointment.

Required Information
Appointment date

The backend identifies the customer using the caller's phone number.

Preconditions

The AI has:

Identified the correct appointment.
Confirmed cancellation with the customer.
Never Call If

Customer

I'm thinking of cancelling.

↓

Ask for confirmation first.

Success Response

Your appointment has been cancelled. Is there anything else I can help you with?

## Reschedule Appointment
Purpose

Move an existing appointment to a new date and/or time.

Required Information
Existing appointment
New preferred date
New preferred time
Customer confirmation
Tool Sequence
check_availability

↓

Customer confirms

↓

reschedule_appointment
Never Call If

Availability hasn't been checked.

## Get Customer Appointment
Purpose

Retrieve the customer's booked appointment.

Required Information
Appointment date (if needed to disambiguate)
Success Response

You have an appointment on Tuesday, July 28 at 10 AM.
