from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Deal:
    id: Optional[int] = None
    client_id: int = 0
    title: str = ""
    value: float = 0.0
    stage: str = "lead"
    owner_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
