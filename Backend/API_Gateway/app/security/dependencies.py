from fastapi import Depends, HTTPException, Request

def require_role(role: str):
    def checker(request: Request):
        user = request.state.user
        if user.get("role") != role:
            raise HTTPException(403, "Insufficient permissions")
    return checker
