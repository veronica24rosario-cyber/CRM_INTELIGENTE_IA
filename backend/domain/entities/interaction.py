from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Interaction:
    id: Optional[int] = None
    client_id: int = 0
    user_id: Optional[int] = None
    type: str = "call"
    subject: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
