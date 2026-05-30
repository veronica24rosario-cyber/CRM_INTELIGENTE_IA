from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Client:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: str = ""
    company: str = ""
    notes: str = ""
    owner_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
