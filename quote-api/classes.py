from dataclasses import dataclass

@dataclass
class Quote:
    shipping_channel: str
    total_cost: float
    cost_breakdown: dict
    shipping_time_range: dict