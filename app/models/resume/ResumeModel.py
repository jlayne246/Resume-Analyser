from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class WorkExperience(BaseModel):
    company: str
    title: str = Field(alias="job_title")
    start_date: str
    end_date: str
    description: str = Field(alias="duties")
    location: Optional[str] = Field(default=None)
    
    class Config:
        populate_by_name = True

class Education(BaseModel):
    institution: str = Field(default=None)
    major: str = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    end_date: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    # Gemini usually omits these → make them optional
    degree: Optional[str] = None
    location: Optional[str] = None
    minor: Optional[str] = None
    details: Optional[str] = None
    gpa: Optional[str] = None
    relevant_coursework: Optional[List[str]] = None

class VolunteerExperience(BaseModel):
    organization: str
    title: str
    start_date: str
    end_date: str
    description: str
    # not always present
    location: Optional[str] = None

class Reference(BaseModel):
    name: str
    title: Optional[str] = None
    company: str
    mobile: Optional[str] = None
    email: EmailStr
    # Gemini doesn’t use "organization" or "phone", so drop them or alias them
    organization: Optional[str] = None
    phone: Optional[str] = None

class Links(BaseModel):
    linkedin: Optional[str] = None
    personal_website: Optional[str] = None
    indeed: Optional[str] = None
    github: Optional[str] = None

class Publication(BaseModel):
    title: str
    publisher: Optional[str] = None
    date: str
    url: Optional[str] = None

class ResumeSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    links: List[Links] = []
    location: str
    objective: Optional[str] = None
    summary: Optional[str] = None
    soft_skills: List[str] = []
    hard_skills: List[str] = []
    work_experience: List[WorkExperience] = []
    education: List[Education] = []
    volunteer_experience: List[VolunteerExperience] = []
    awards: List[str] = []
    publications: List[Publication] = []
    certifications: List[str] = []
    references: List[Reference] = []
