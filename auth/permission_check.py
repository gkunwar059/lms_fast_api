from typing import Any
from models import User
from fastapi import Depends, HTTPException
from models import Role


class RoleCheck:
    def __init__(self, allowed_permission):
        """constructor of the rolecheck class"""
        self.allowed_permission = allowed_permission

    def __call__(self, user=Depends(User.get_current_user)):
        """when we call RoleCheck class ,this call method(function) is called first"""

        for users_role in self.allowed_permission:
            if users_role not in (
                Role.get_permission(user["role"])
            ):  # deyako role ma chai mathi haleko permission xaina vane chai exception gar ,yedi deyako role ma chai permission xa vane chai user return gardinu hai ta

                raise HTTPException(
                    status_code=401, detail="You don't permission to access ! "
                )

        return user
