"""Incident repository — async CRUD operations."""

from sqlalchemy import select

from app.db.config import get_session_factory
from app.db.models import Incident, IncidentStatus


async def create_incident(
    incident_id: str,
    title: str,
    description: str,
    reporter_email: str,
    attachments: list[str] | None = None,
) -> Incident:
    factory = get_session_factory()
    incident = Incident(
        id=incident_id,
        title=title,
        description=description,
        reporter_email=reporter_email,
        attachments=attachments,
    )
    async with factory() as session:
        session.add(incident)
        await session.commit()
        await session.refresh(incident)
    return incident


async def get_incident(incident_id: str) -> Incident | None:
    factory = get_session_factory()
    async with factory() as session:
        return await session.get(Incident, incident_id)


async def update_incident(incident_id: str, **fields: object) -> Incident | None:
    factory = get_session_factory()
    async with factory() as session:
        incident = await session.get(Incident, incident_id)
        if incident is None:
            return None
        for key, value in fields.items():
            setattr(incident, key, value)
        await session.commit()
        await session.refresh(incident)
    return incident


async def list_incidents(
    status: IncidentStatus | None = None,
    limit: int = 50,
) -> list[Incident]:
    factory = get_session_factory()
    async with factory() as session:
        stmt = select(Incident).order_by(Incident.created_at.desc()).limit(limit)
        if status is not None:
            stmt = stmt.where(Incident.status == status)
        result = await session.execute(stmt)
        return list(result.scalars().all())
