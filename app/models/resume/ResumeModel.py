from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional   

class WorkExperience(BaseModel):
    company: str
    location: Optional[str]
    job_title: str
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    
class VolunteerExperience(BaseModel):
    entity: str
    location: Optional[str]
    role: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]

class Education(BaseModel):
    institution: str
    location: Optional[str]
    degree: Optional[str]
    major: Optional[str]
    minor: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    details: Optional[str]
    gpa: Optional[float]
    
class Links(BaseModel):
    linkedin: Optional[str]
    personal_website: Optional[str]
    indeed: Optional[str]
    github: Optional[str]
    
class Reference(BaseModel):
    name: str
    title: str
    organization: str
    phone: str
    email: str

class ResumeSchema(BaseModel):
    first_name: str = Field(..., description="First name of the individual")
    last_name: str = Field(..., description="Last name of the individual")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    links: Optional[Links] = Field(None, description="List of relevant links (e.g., LinkedIn, personal website)")
    location: Optional[str] = Field(None, description="Location or address")
    objective: Optional[str] = Field(None, description="Career objective or summary")
    summary: Optional[str] = Field(None, description="Professional summary or objective")
    soft_skills: List[str] = Field(default_factory=list, description="List of soft skills")
    hard_skills: List[str] = Field(default_factory=list, description="List of hard skills")
    work_experience: List[WorkExperience] = Field(default_factory=list, description="Work experience details")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    volunteer_experience: Optional[List[VolunteerExperience]] = Field(None, description="Volunteer experience details")
    awards: Optional[List[str]] = Field(None, description="Awards and recognitions")
    publications: Optional[List[str]] = Field(None, description="Publications details")
    certifications: Optional[List[str]] = Field(None, description="Certifications and licenses")
    references: Optional[List[Reference]] = Field(None, description="References details")

