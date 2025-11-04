from pydantic import BaseModel, EmailStr
from typing import List, Optional

class WorkExperience(BaseModel):
    company: Optional[str]
    title: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    location: Optional[str] = None  # Gemini often omits this

class Education(BaseModel):
    institution: Optional[str]
    major: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    # Gemini usually omits these → make them optional
    degree: Optional[str] = None
    location: Optional[str] = None
    minor: Optional[str] = None
    details: Optional[str] = None
    gpa: Optional[str] = None

class VolunteerExperience(BaseModel):
    organization: Optional[str]
    title: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    # not always present
    location: Optional[str] = None

class Reference(BaseModel):
    name: Optional[str]
    title: Optional[str]
    company: Optional[str]
    mobile: Optional[str]
    email: Optional[EmailStr]
    # Gemini doesn’t use "organization" or "phone", so drop them or alias them
    organization: Optional[str] = None
    phone: Optional[str] = None

class Links(BaseModel):
    linkedin: Optional[str]
    personal_website: Optional[str]
    indeed: Optional[str]
    github: Optional[str]

class ResumeSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    links: Optional[Links]
    location: Optional[str]
    objective: Optional[str]
    summary: Optional[str]
    soft_skills: List[str] = []
    hard_skills: List[str] = []
    work_experience: List[WorkExperience] = []
    education: List[Education] = []
    volunteer_experience: List[VolunteerExperience] = []
    awards: List[str] = []
    publications: List[str] = []
    certifications: List[str] = []
    references: List[Reference] = []
