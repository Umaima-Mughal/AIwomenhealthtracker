from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Tracking(Base):
    __tablename__ = "tracking_records"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    date = Column(Date, nullable=False, index=True)

    # General health tracking
    symptoms = Column(Text, nullable=True)
    mood = Column(String, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)

    # Menstrual/cycle tracking
    cycle_day = Column(Integer, nullable=True)
    period_started = Column(String, nullable=True)

    # Additional notes
    notes = Column(Text, nullable=True)

    user = relationship("User", backref="tracking_records")