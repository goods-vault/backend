from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declarative_mixin


class Base(DeclarativeBase):
    pass

@declarative_mixin
class CreatedAtMixin:
    """Model mixin that adds 'created_at' field"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

@declarative_mixin
class UpdatedAtMixin:
    """Model mixin that adds 'updated_at' field"""
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]

    parent: Mapped[Optional["Category"]] = relationship(back_populates="children", remote_side="Category.id")
    children: Mapped[list["Category"]] = relationship(back_populates="parent")

    def __repr__(self):
        return f"<Category(id={self.id}, parent_id={self.parent_id}, title={self.title})>"


class Product(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "products"

    gtin: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    brand: Mapped[str | None]
    title: Mapped[str]
    image: Mapped[str | None]
    net_content_unit: Mapped[str | None]
    net_content_value: Mapped[float | None]
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    updated_in_gs1_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    category: Mapped["Category"] = relationship(backref="products", lazy="joined")

    @property
    def net_content(self) -> dict:
        return {
            "unit": self.net_content_unit,
            "value": self.net_content_value,
        }

    @property
    def category_title(self) -> str:
        return self.category.title
