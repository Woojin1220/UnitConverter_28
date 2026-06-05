from entity.registry import get_to_meter_ratio


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    in_meters = value * get_to_meter_ratio(from_unit)
    return in_meters / get_to_meter_ratio(to_unit)
