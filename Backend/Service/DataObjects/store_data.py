from dataclasses import dataclass


@dataclass
class StoreData:
    id: str
    name: str
    ids_to_quantities: dict[str, int]