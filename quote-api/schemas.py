from marshmallow import Schema, fields

class BoxSchema(Schema):
    count = fields.Int(required=True, load_only=True)
    weight_kg = fields.Float(required=True, load_only=True)
    length = fields.Float(required=True, load_only=True)
    width = fields.Float(required=True, load_only=True)
    height = fields.Float(required=True, load_only=True)

class QuoteCostBreakDownSchema(Schema):
    shipping_cost = fields.Float(required=True)
    service_fee = fields.Float(required=True)
    oversized_fee = fields.Float(required=True)
    overweight_fee = fields.Float(required=True)

class QuoteShippingTimeRangeSchema(Schema):
    min_days = fields.Integer(required=True)
    max_days = fields.Integer(required=True)

class QuoteSchema(Schema):
    shipping_channel = fields.Str(required=True, dump_only=True)
    total_cost = fields.Float(required=True, dump_only=True)
    cost_breakdown = fields.Nested(QuoteCostBreakDownSchema, required=True, dump_only=True)
    shipping_time_range = fields.Nested(QuoteShippingTimeRangeSchema, required=True, dump_only=True)

class GetShippingQuotesSchema(Schema):
    starting_country = fields.Str(required=True, load_only=True)
    destination_country = fields.Str(required=True, load_only=True)
    boxes = fields.List(fields.Nested(BoxSchema), required=True, load_only=True)
    quotes = fields.List(fields.Nested(QuoteSchema), required=True, dump_only=True)