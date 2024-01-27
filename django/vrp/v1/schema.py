from datetime import date, datetime
from ninja import Schema
from typing import List

class DestinationSchema(Schema):
    address1: str
    address2: str
    city: str
    company: str
    country: str
    email: str
    first_name: str
    last_name: str
    phone: str
    province: str
    zip: str
    latitude: float
    longitude: float

class FulfillmentLineItemSchema(Schema):
    line_item_id: str
    channel_id: str
    quantity: int
    delivered: bool
    delivered_at: datetime

class FulfillmentSchema(Schema):
    id: str
    channel_id: str
    created_at: datetime
    updated_at: datetime
    delivered_at: datetime
    display_status: str
    in_transit_at: datetime
    name: str
    status: str
    shipment_status: str
    total_quantity: int
    fulfillment_tracking_company: str
    fulfillment_tracking_numbers: str
    fulfillment_tracking_urls: str
    note: str
    email_notification: bool
    sms_notification: bool
    delivered: bool
    destination: DestinationSchema
    fulfillment_line_items: List[FulfillmentLineItemSchema]


class FulfillmentInSchema(FulfillmentSchema):
    destination: int
    fulfillment_line_items: List[int]

class FulfillmentOutSchema(FulfillmentSchema):
    pass

class FulfillmentUpdateSchema(Schema):
    channel_id: str = None
    created_at: datetime = None
    updated_at: datetime = None
    delivered_at: datetime = None
    display_status: str = None
    in_transit_at: datetime = None
    name: str = None
    status: str = None
    shipment_status: str = None
    total_quantity: int = None
    fulfillment_tracking_company: str = None
    fulfillment_tracking_numbers: str = None
    fulfillment_tracking_urls: str = None
    note: str = None
    email_notification: bool = None
    sms_notification: bool = None
    delivered: bool = None


class RouteRequestSchema(Schema):
    vehicle_ids: List[int]
    fulfillment_ids: List[str]
    planned_date: datetime

class SkillIn(Schema):
    description: str

class SkillOut(Schema):
    id: int
    description: str

class VehicleIn(Schema):
    skills: List[int]
    capacity: List[int]

class VehicleOut(Schema):
    id: int
    skills: List[SkillOut]
    capacity: List[int]


