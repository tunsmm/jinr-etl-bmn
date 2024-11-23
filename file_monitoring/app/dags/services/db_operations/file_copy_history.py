from sqlalchemy.orm import Session
from models.db import FileCopyHistory
from datetime import datetime


def create_file_copy_history(session: Session, file_name: str, file_size: int, file_hash_before: str):
    """Создание новой записи в истории копирования файлов."""
    history_entry = FileCopyHistory(
        file_name=file_name,
        file_size=file_size,
        file_hash_before=file_hash_before,
        copy_started_at=datetime.now()
    )
    session.add(history_entry)
    session.commit()
    return history_entry.id  # Возвращаем ID созданной записи


def update_file_copy_history(session: Session, entry_id: int, file_hash_after: str):
    """Обновление записи в истории копирования файлов."""
    history_entry = session.query(FileCopyHistory).filter(FileCopyHistory.id == entry_id).first()
    if history_entry:
        history_entry.file_hash_after = file_hash_after
        history_entry.copy_ended_at = datetime.now()
        session.commit()
