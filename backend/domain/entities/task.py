from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: Optional[int] = None
    client_id: Optional[int] = None
    title: str = ""
    description: str = ""
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
