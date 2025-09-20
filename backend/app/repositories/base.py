from typing import Generic, TypeVar, Type, Optional, List, Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.db.base_class import Base
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository with model class
        """
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Get a single record by ID
        """
        return db.execute(
            select(self.model).filter(self.model.id == id)
        ).scalar_one_or_none()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Dict[str, Any] = None
    ) -> List[ModelType]:
        """
        Get multiple records with optional filtering
        """
        query = select(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)
        
        return list(db.execute(query.offset(skip).limit(limit)).scalars().all())
    
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create a new record
        """
        obj_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        id: int,
        obj_in: Union[Dict[str, Any], ModelType]
    ) -> Optional[ModelType]:
        """
        Update a record
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = jsonable_encoder(obj_in)
        
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
            .returning(self.model)
        )
        result = db.execute(stmt)
        db.commit()
        return result.scalar_one_or_none()
    
    def delete(self, db: Session, *, id: int) -> bool:
        """
        Delete a record
        """
        stmt = delete(self.model).where(self.model.id == id)
        result = db.execute(stmt)
        db.commit()
        return result.rowcount > 0
    
    def exists(self, db: Session, id: int) -> bool:
        """
        Check if a record exists
        """
        stmt = select(self.model).filter(self.model.id == id)
        result = db.execute(stmt)
        return result.first() is not None