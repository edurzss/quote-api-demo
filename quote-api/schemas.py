from marshmallow import Schema, fields

class BoxSchema(Schema):
    count = fields.Int(required=True)
    weight_kg = fields.Float(required=True)
    length = fields.Float(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)

class QuoteSchema(Schema):
    shipping_channel = fields.Str(required=True)
    total_cost = fields.Float(required=True)
    cost_breakdown = fields.Dict(keys=fields.Str(), values=fields.Float(), required=True)
    shipping_time_range = fields.Dict(keys=fields.Str(), values=fields.Int(), required=True)

class GetShippingQuotesSchema(Schema):
    starting_country = fields.Str(required=True, load_only=True)
    destination_country = fields.Str(required=True, load_only=True)
    boxes = fields.List(fields.Nested(BoxSchema), required=True, load_only=True)
    quotes = fields.List(fields.Nested(QuoteSchema), required=True, dump_only=True)