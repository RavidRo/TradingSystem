from __future__ import annotations

from typing import List


class ResponsibilitiesData:
    def __init__(
        self,
        store_id: str,
        is_manager: bool,
        permissions: List[str],
        role: str,
        appointees: List[ResponsibilitiesData],
    ) -> None:

        self.store_id = store_id
        self.is_manager = is_manager
        self.role = role
        self.appointees = appointees
        self.permissions = permissions
