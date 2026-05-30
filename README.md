# Wheelie
Bike rental management system.

## Data model notes
- Rentals track returns via `rental_end`, `total_amount`, and `status` (`active`, `overdue`, `returned`). There is no separate returns table.
- Payments reference rentals through `payment.rental_id` (no `customer_id`/`bike_id` columns on payments).
- Customers track the registering staff member via `customer.staff_id` and store valid ID file paths in `customer.valid_id`.
- Bikes include `bike_rate` and `type` fields for pricing and categorization.
