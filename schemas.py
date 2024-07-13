from pydantic import BaseModel
from typing import Optional


class PoliticianRecord(BaseModel):
    id: str
    label: str = "politician"
    literal: str
    uri: str
    positionLabel: Optional[str] = ""
    politicianLabel: Optional[str] = ""
    countryLabel: Optional[str] = ""
    partyLabel: Optional[str] = ""
    twitter: Optional[str] = ""
    instagram: Optional[str] = ""
    facebook: Optional[str] = ""
