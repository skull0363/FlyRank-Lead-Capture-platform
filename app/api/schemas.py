from pydantic import BaseModel, EmailStr, Field, constr
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, constr


class WidgetField(BaseModel):
    name: str
    type: str  # text | email | textarea
    required: bool = False

class WidgetCreate(BaseModel):
    type: str = Field(..., pattern="^(signup_form|cta|popover)$")
    title: constr(min_length=1, max_length=100)
    description: constr(max_length=500) = ""
    fields: List[WidgetField]
    button_text: constr(max_length=50) = "Submit"
    display_options: Dict[str, Any] = {}

class SubmissionCreate(BaseModel):
    widget_id: str
    data: Dict[str, Any]
    honeypot: Optional[str] = ""  # spam trap field, must stay empty

    class Config:
        # reject payloads with too many fields / oversized strings
        pass



class TenantRegister(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    password: constr(min_length=8, max_length=128)


class TenantLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=1, max_length=128)