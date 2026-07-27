from sqlalchemy.orm import Session

from app.models.audit_logs import AuditLog



def create_audit_log(
    db: Session,
    user_id: int | None,
    action: str,
    module: str,
    old_data: dict | None = None,
    new_data: dict | None = None,
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        module=module,
        old_data=old_data,
        new_data=new_data,
    )

    db.add(audit_log)

    return audit_log