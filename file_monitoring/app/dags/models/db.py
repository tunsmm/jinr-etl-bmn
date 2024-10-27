from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

# Define a base class for declarative class definitions
Base = declarative_base()


class FileCopyHistory(Base):
    __tablename__ = "file_copy_history"

    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    file_hash_before = Column(String(255), nullable=False)
    file_hash_after = Column(String(255), nullable=True)

    copy_started_at = Column(DateTime, nullable=False)
    copy_ended_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f"<FileCopyHistory>(id={self.id}, name={self.file_name}, size={self.file_size}, "
            f"created_at={self.file_created_at}, started_at={self.copy_started_at}, "
            f"copy_ended_at={self.copy_ended_at}, "
            f"file_hash: before={self.file_hash_before}, after={self.file_hash_after})"
        )
