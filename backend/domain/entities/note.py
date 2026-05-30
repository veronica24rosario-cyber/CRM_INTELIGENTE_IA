from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Note:
    id: Optional[int] = None
    client_id: int = 0
    content: str = ""
    created_by: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
