from __future__ import annotations

from sqlalchemy import ForeignKey, String, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    coordinates: Mapped[str] = mapped_column(JSON, nullable=False)

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        back_populates="building",
        cascade="all, delete-orphan"
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"), nullable=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    parent: Mapped[Activity | None] = relationship(
        "Activity",
        remote_side=[id],
        back_populates="children"
    )
    children: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organization_activities",
        back_populates="activities"
    )


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phones: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building: Mapped["Building"] = relationship(
        "Building",
        back_populates="organizations"
    )

    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activities",
        back_populates="organizations"
    )


class OrganizationActivity(Base):
    __tablename__ = "organization_activities"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        primary_key=True
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id"),
        primary_key=True
    )
