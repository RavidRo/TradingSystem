from __future__ import annotations

from typing import List


class ResponsibilitiesData:
    def __init__(
        self,
        store_id: str,
        store_name: str,
        is_manager: bool,
        role: str,
        appointees: List[ResponsibilitiesData],
        permissions: List[str],
        username: str,
    ) -> None:

        self.store_id = store_id
        self.is_manager = is_manager
        self.role = role
        self.appointees = appointees
        self.permissions = permissions
        self.username = username
        self.store_name = store_name
