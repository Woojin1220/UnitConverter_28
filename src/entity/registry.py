from entity.constants import DEFAULT_UNITS

_units: dict[str, float] = dict(DEFAULT_UNITS)


def register_unit(name: str, to_meter_ratio: float) -> None:
    _units[name] = to_meter_ratio


def get_registered_units() -> dict[str, float]:
    return dict(_units)


def get_to_meter_ratio(unit: str) -> float:
    return _units[unit]


def reset_registry() -> None:
    global _units
    _units = dict(DEFAULT_UNITS)
