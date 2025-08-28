from fastapi import HTTPException,status


def check_creator(creator_id: int, payload: dict, subject: str):
    supplier_id = int(payload.get("sub"))
    roles = payload.get("roles")

    if creator_id != supplier_id and "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access to modify the {subject} is denied"
        )
