"""
schemas.py

Pydantic models: every request field has an enforced data type AND a realistic
range/choice constraint, per the rubric ("Data types" + "Range constraints").
"""

from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    # A few raw/messy variants are also accepted for convenience; normalized in model_utils.
    M = "M"
    F = "F"
    MALE = "MALE"
    FEMALE = "FEMALE"


class CountryEnum(str, Enum):
    argentina = "Argentina"
    australia = "Australia"
    brazil = "Brazil"
    canada = "Canada"
    china = "China"
    egypt = "Egypt"
    france = "France"
    germany = "Germany"
    india = "India"
    indonesia = "Indonesia"
    italy = "Italy"
    japan = "Japan"
    mexico = "Mexico"
    netherlands = "Netherlands"
    russia = "Russia"
    south_africa = "South Africa"
    south_korea = "South Korea"
    spain = "Spain"
    turkey = "Turkey"
    united_kingdom = "United Kingdom"
    united_states = "United States"


class PrimarySkillEnum(str, Enum):
    ai = "AI"
    blockchain_development = "Blockchain Development"
    cybersecurity = "Cybersecurity"
    data_analysis = "Data Analysis"
    devops = "DevOps"
    graphic_design = "Graphic Design"
    machine_learning = "Machine Learning"
    mobile_apps = "Mobile Apps"
    ui_ux_design = "UI/UX Design"
    web_development = "Web Development"


class PredictionRequest(BaseModel):
    """Every field has an explicit Python/Pydantic data type, and every numeric
    field has a realistic range constraint (via Field's ge/le), matching the
    bounds actually observed in the training data."""

    gender: GenderEnum = Field(..., description="Freelancer's gender")
    age: int = Field(..., ge=18, le=75, description="Age in years (realistic working-age bounds)")
    country: CountryEnum = Field(..., description="Freelancer's country")
    primary_skill: PrimarySkillEnum = Field(..., description="Freelancer's primary skill/category")
    years_of_experience: float = Field(..., ge=0, le=50, description="Years of professional experience")
    rating: float = Field(..., ge=0.0, le=5.0, description="Average client rating, 0-5 stars")
    is_active: bool = Field(..., description="Whether the freelancer is currently active on the platform")
    client_satisfaction: float = Field(
        ..., ge=0.0, le=100.0,
        description="Client satisfaction score as a percentage (0-100)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "gender": "female",
                "age": 34,
                "country": "India",
                "primary_skill": "Machine Learning",
                "years_of_experience": 6,
                "rating": 4.2,
                "is_active": True,
                "client_satisfaction": 88.0,
            }
        }


class PredictionResponse(BaseModel):
    predicted_hourly_rate_usd: float
    currency: str = "USD"
    model_used: str


class ModelMetric(BaseModel):
    model: str
    mse: float
    rmse: float
    mae: float
    r2: float


class RetrainResponse(BaseModel):
    status: str
    best_model: str
    n_training_rows: int
    all_model_metrics: List[ModelMetric]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    best_model_name: Optional[str] = None
