from dataclasses import dataclass


@dataclass(eq=False)        # I don't know exactly what is eq here but now StoreData is hashable :)
class StoreData:
    id: str
    name: str
    ids_to_quantities: dict[str, int]
