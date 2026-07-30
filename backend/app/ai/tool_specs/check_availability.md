
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
