from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class WorkExperience(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = Field(default=None, alias="job_title")
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = Field(default=None, alias="duties")
    location: Optional[str] = Field(default=None)
    
    class Config:
        populate_by_name = True

class Education(BaseModel):
    institution: str = Optional[str] = Field(default=None)
    major: str = Optional[str] = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    end_date: str = Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    # Gemini usually omits these → make them optional
    degree: Optional[str] = None
    location: Optional[str] = None
    minor: Optional[str] = None
    details: Optional[str] = None
    gpa: Optional[str] = None
    relevant_coursework: Optional[List[str]] = None

class VolunteerExperience(BaseModel):
    organization: Optional[str] = None
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    # not always present
    location: Optional[str] = None

class Reference(BaseModel):
    name: Optional[str]
    title: Optional[str] = None
    company: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    # Gemini doesn’t use "organization" or "phone", so drop them or alias them
    organization: Optional[str] = None
    phone: Optional[str] = None

class Links(BaseModel):
    linkedin: Optional[str] = None
    personal_website: Optional[str] = None
    indeed: Optional[str] = None
    github: Optional[str] = None

class Publication(BaseModel):
    title: Optional[str] = None
    publisher: Optional[str] = None
    date: Optional[str] = None
    url: Optional[str] = None

class ResumeSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    links: Optional[Links] = None
    address: Optional[str] = None
    objective: Optional[str] = None
    summary: Optional[str] = None
    soft_skills: Optional[List[str]] = None
    hard_skills: Optional[List[str]] = None
    work_experience: Optional[List[WorkExperience]] = None
    education: Optional[List[Education]] = None
    volunteer_experience: Optional[List[VolunteerExperience]] = None
    awards: Optional[List[str]] = None
    publications: Optional[List[Publication]] = None
    certifications: Optional[List[str]] = None
    references: Optional[List[Reference]] = None

#test