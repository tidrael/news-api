from database import Base
from sqlalchemy import Boolean, Column, Integer, String, Text


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    day = Column(String(255), nullable=False)
    title = Column(Text, nullable=False)
    checked = Column(Boolean, default=False)
    classification = Column(String(255), nullable=True)

    def __repr__(self):
        return f"{self.title}"
