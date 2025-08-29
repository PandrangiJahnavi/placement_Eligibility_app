from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
import sqlite3
from faker import Faker
import pandas as pd

# Enums for better type safety and validation
class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class PlacementStatus(Enum):
    READY = "Ready"
    NOT_READY = "Not Ready"
    PLACED = "Placed"

class ProgrammingLanguage(Enum):
    PYTHON = "Python"
    SQL = "SQL"
    JAVA = "Java"
    JAVASCRIPT = "JavaScript"

# Data Classes for each table
@dataclass
class Student:
    """Student data structure with validation and methods"""
    student_id: int
    name: str
    age: int
    gender: Gender
    email: str
    phone: str
    enrollment_year: int
    course_batch: str
    city: str
    graduation_year: int
    
    def __post_init__(self):
        """Validate data after initialization"""
        if not (18 <= self.age <= 35):
            raise ValueError("Age must be between 18 and 35")
        if self.graduation_year < self.enrollment_year:
            raise ValueError("Graduation year cannot be before enrollment year")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender.value,
            'email': self.email,
            'phone': self.phone,
            'enrollment_year': self.enrollment_year,
            'course_batch': self.course_batch,
            'city': self.city,
            'graduation_year': self.graduation_year
        }

@dataclass
class Programming:
    """Programming performance data structure"""
    programming_id: int
    student_id: int
    language: ProgrammingLanguage
    problems_solved: int
    assessments_completed: int
    mini_projects: int
    certifications_earned: int
    latest_project_score: float
    
    def __post_init__(self):
        """Validate programming data"""
        if not (0 <= self.latest_project_score <= 100):
            raise ValueError("Project score must be between 0 and 100")
        if any(val < 0 for val in [self.problems_solved, self.assessments_completed, 
                                  self.mini_projects, self.certifications_earned]):
            raise ValueError("All counts must be non-negative")
    
    def performance_score(self) -> float:
        """Calculate overall programming performance score"""
        weights = {
            'problems': 0.3,
            'assessments': 0.25,
            'projects': 0.25,
            'certifications': 0.1,
            'latest_score': 0.1
        }
        
        # Normalize values (assuming max values)
        normalized_problems = min(self.problems_solved / 100, 1.0)
        normalized_assessments = min(self.assessments_completed / 20, 1.0)
        normalized_projects = min(self.mini_projects / 10, 1.0)
        normalized_certs = min(self.certifications_earned / 5, 1.0)
        normalized_score = self.latest_project_score / 100
        
        return (weights['problems'] * normalized_problems +
                weights['assessments'] * normalized_assessments +
                weights['projects'] * normalized_projects +
                weights['certifications'] * normalized_certs +
                weights['latest_score'] * normalized_score) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'programming_id': self.programming_id,
            'student_id': self.student_id,
            'language': self.language.value,
            'problems_solved': self.problems_solved,
            'assessments_completed': self.assessments_completed,
            'mini_projects': self.mini_projects,
            'certifications_earned': self.certifications_earned,
            'latest_project_score': self.latest_project_score
        }

@dataclass
class SoftSkills:
    """Soft skills data structure with score validation"""
    soft_skill_id: int
    student_id: int
    communication: float
    teamwork: float
    presentation: float
    leadership: float
    critical_thinking: float
    interpersonal_skills: float
    
    def __post_init__(self):
        """Validate all scores are between 0 and 100"""
        scores = [self.communication, self.teamwork, self.presentation,
                 self.leadership, self.critical_thinking, self.interpersonal_skills]
        
        for score in scores:
            if not (0 <= score <= 100):
                raise ValueError(f"All skill scores must be between 0 and 100")
    
    def average_score(self) -> float:
        """Calculate average soft skills score"""
        scores = [self.communication, self.teamwork, self.presentation,
                 self.leadership, self.critical_thinking, self.interpersonal_skills]
        return sum(scores) / len(scores)
    
    def get_strengths(self, threshold: float = 80.0) -> List[str]:
        """Get list of strength areas (scores above threshold)"""
        skills_map = {
            'communication': self.communication,
            'teamwork': self.teamwork,
            'presentation': self.presentation,
            'leadership': self.leadership,
            'critical_thinking': self.critical_thinking,
            'interpersonal_skills': self.interpersonal_skills
        }
        
        return [skill for skill, score in skills_map.items() if score >= threshold]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'soft_skill_id': self.soft_skill_id,
            'student_id': self.student_id,
            'communication': self.communication,
            'teamwork': self.teamwork,
            'presentation': self.presentation,
            'leadership': self.leadership,
            'critical_thinking': self.critical_thinking,
            'interpersonal_skills': self.interpersonal_skills
        }

@dataclass
class Placement:
    """Placement data structure with comprehensive tracking"""
    placement_id: int
    student_id: int
    mock_interview_score: float
    internships_completed: int
    placement_status: PlacementStatus
    company_name: Optional[str] = None
    placement_package: Optional[float] = None
    interview_rounds_cleared: int = 0
    placement_date: Optional[date] = None
    
    def __post_init__(self):
        """Validate placement data"""
        if not (0 <= self.mock_interview_score <= 100):
            raise ValueError("Mock interview score must be between 0 and 100")
        if self.internships_completed < 0:
            raise ValueError("Internships completed cannot be negative")
        if self.placement_status == PlacementStatus.PLACED:
            if not self.company_name or not self.placement_package:
                raise ValueError("Placed students must have company name and package")
    
    def is_placement_ready(self, min_interview_score: float = 70.0, 
                          min_internships: int = 1) -> bool:
        """Check if student meets placement readiness criteria"""
        return (self.mock_interview_score >= min_interview_score and 
                self.internships_completed >= min_internships)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'placement_id': self.placement_id,
            'student_id': self.student_id,
            'mock_interview_score': self.mock_interview_score,
            'internships_completed': self.internships_completed,
            'placement_status': self.placement_status.value,
            'company_name': self.company_name,
            'placement_package': self.placement_package,
            'interview_rounds_cleared': self.interview_rounds_cleared,
            'placement_date': self.placement_date.isoformat() if self.placement_date else None
        }

# Main Database Manager Class
class PlacementDatabase:
    """Database manager with OOP principles for the placement eligibility system"""
    
    def __init__(self, db_path: str = "placement_eligibility.db"):
        self.db_path = db_path
        self.fake = Faker()
        self.create_tables()
    
    def create_tables(self):
        """Create all required tables with proper relationships"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT NOT NULL,
                    enrollment_year INTEGER NOT NULL,
                    course_batch TEXT NOT NULL,
                    city TEXT NOT NULL,
                    graduation_year INTEGER NOT NULL
                )
            ''')
            
            # Programming table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS programming (
                    programming_id INTEGER PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    problems_solved INTEGER NOT NULL,
                    assessments_completed INTEGER NOT NULL,
                    mini_projects INTEGER NOT NULL,
                    certifications_earned INTEGER NOT NULL,
                    latest_project_score REAL NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students (student_id)
                )
            ''')
            
            # Soft skills table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS soft_skills (
                    soft_skill_id INTEGER PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    communication REAL NOT NULL,
                    teamwork REAL NOT NULL,
                    presentation REAL NOT NULL,
                    leadership REAL NOT NULL,
                    critical_thinking REAL NOT NULL,
                    interpersonal_skills REAL NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students (student_id)
                )
            ''')
            
            # Placements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS placements (
                    placement_id INTEGER PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    mock_interview_score REAL NOT NULL,
                    internships_completed INTEGER NOT NULL,
                    placement_status TEXT NOT NULL,
                    company_name TEXT,
                    placement_package REAL,
                    interview_rounds_cleared INTEGER DEFAULT 0,
                    placement_date TEXT,
                    FOREIGN KEY (student_id) REFERENCES students (student_id)
                )
            ''')
            
            conn.commit()
    
    def generate_sample_data(self, num_students: int = 100):
        """Generate sample data using Faker library"""
        students = []
        programming_records = []
        soft_skills_records = []
        placement_records = []
        
        # Generate students
        for i in range(1, num_students + 1):
            student = Student(
                student_id=i,
                name=self.fake.name(),
                age=self.fake.random_int(min=20, max=28),
                gender=self.fake.random_element(elements=[Gender.MALE, Gender.FEMALE, Gender.OTHER]),
                email=self.fake.email(),
                phone=self.fake.phone_number(),
                enrollment_year=self.fake.random_int(min=2020, max=2024),
                course_batch=f"Batch_{self.fake.random_element(elements=['A', 'B', 'C', 'D'])}_{self.fake.random_int(min=2020, max=2024)}",
                city=self.fake.city(),
                graduation_year=self.fake.random_int(min=2024, max=2026)
            )
            students.append(student)
            
            # Generate programming record for each student
            programming = Programming(
                programming_id=i,
                student_id=i,
                language=self.fake.random_element(elements=list(ProgrammingLanguage)),
                problems_solved=self.fake.random_int(min=10, max=150),
                assessments_completed=self.fake.random_int(min=3, max=25),
                mini_projects=self.fake.random_int(min=1, max=12),
                certifications_earned=self.fake.random_int(min=0, max=8),
                latest_project_score=self.fake.random.uniform(60, 100)
            )
            programming_records.append(programming)
            
            # Generate soft skills record
            soft_skills = SoftSkills(
                soft_skill_id=i,
                student_id=i,
                communication=self.fake.random.uniform(50, 100),
                teamwork=self.fake.random.uniform(50, 100),
                presentation=self.fake.random.uniform(40, 100),
                leadership=self.fake.random.uniform(45, 100),
                critical_thinking=self.fake.random.uniform(55, 100),
                interpersonal_skills=self.fake.random.uniform(50, 100)
            )
            soft_skills_records.append(soft_skills)
            
            # Generate placement record
            status = self.fake.random_element(elements=list(PlacementStatus))
            company = self.fake.company() if status == PlacementStatus.PLACED else None
            package = self.fake.random.uniform(40000, 120000) if status == PlacementStatus.PLACED else None
            placement_date = self.fake.date_between(start_date='-1y', end_date='today') if status == PlacementStatus.PLACED else None
            
            placement = Placement(
                placement_id=i,
                student_id=i,
                mock_interview_score=self.fake.random.uniform(45, 100),
                internships_completed=self.fake.random_int(min=0, max=4),
                placement_status=status,
                company_name=company,
                placement_package=package,
                interview_rounds_cleared=self.fake.random_int(min=0, max=5),
                placement_date=placement_date
            )
            placement_records.append(placement)
        
        # Insert all data into database
        self.insert_students(students)
        self.insert_programming_records(programming_records)
        self.insert_soft_skills_records(soft_skills_records)
        self.insert_placement_records(placement_records)
        
        return {
            'students': len(students),
            'programming': len(programming_records),
            'soft_skills': len(soft_skills_records),
            'placements': len(placement_records)
        }
    
    def insert_students(self, students: List[Student]):
        """Insert student records into database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            student_data = [tuple(student.to_dict().values()) for student in students]
            cursor.executemany('''
                INSERT OR REPLACE INTO students 
                (student_id, name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', student_data)
            conn.commit()
    
    def insert_programming_records(self, programming_records: List[Programming]):
        """Insert programming records into database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            prog_data = [tuple(prog.to_dict().values()) for prog in programming_records]
            cursor.executemany('''
                INSERT OR REPLACE INTO programming 
                (programming_id, student_id, language, problems_solved, assessments_completed, 
                 mini_projects, certifications_earned, latest_project_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', prog_data)
            conn.commit()
    
    def insert_soft_skills_records(self, soft_skills_records: List[SoftSkills]):
        """Insert soft skills records into database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            skills_data = [tuple(skills.to_dict().values()) for skills in soft_skills_records]
            cursor.executemany('''
                INSERT OR REPLACE INTO soft_skills 
                (soft_skill_id, student_id, communication, teamwork, presentation, 
                 leadership, critical_thinking, interpersonal_skills)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', skills_data)
            conn.commit()
    
    def insert_placement_records(self, placement_records: List[Placement]):
        """Insert placement records into database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            placement_data = []
            for placement in placement_records:
                data = placement.to_dict()
                placement_data.append(tuple(data.values()))
            
            cursor.executemany('''
                INSERT OR REPLACE INTO placements 
                (placement_id, student_id, mock_interview_score, internships_completed, 
                 placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', placement_data)
            conn.commit()
    
    def get_eligible_students(self, criteria: Dict[str, Any]) -> pd.DataFrame:
        """
        Get students who meet the specified eligibility criteria
        
        Example criteria:
        {
            'min_problems_solved': 50,
            'min_soft_skills_avg': 75,
            'min_mock_interview': 70,
            'min_internships': 1,
            'programming_language': 'Python'
        }
        """
        with sqlite3.connect(self.db_path) as conn:
            # Build dynamic query based on criteria
            base_query = '''
                SELECT 
                    s.student_id, s.name, s.age, s.email, s.course_batch, s.city,
                    p.language, p.problems_solved, p.assessments_completed, p.mini_projects,
                    p.latest_project_score,
                    (ss.communication + ss.teamwork + ss.presentation + 
                     ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6 as avg_soft_skills,
                    pl.mock_interview_score, pl.internships_completed, pl.placement_status,
                    pl.company_name, pl.placement_package
                FROM students s
                JOIN programming p ON s.student_id = p.student_id
                JOIN soft_skills ss ON s.student_id = ss.student_id
                JOIN placements pl ON s.student_id = pl.student_id
                WHERE 1=1
            '''
            
            params = []
            
            if 'min_problems_solved' in criteria:
                base_query += ' AND p.problems_solved >= ?'
                params.append(criteria['min_problems_solved'])
            
            if 'min_soft_skills_avg' in criteria:
                base_query += ' AND (ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6 >= ?'
                params.append(criteria['min_soft_skills_avg'])
            
            if 'min_mock_interview' in criteria:
                base_query += ' AND pl.mock_interview_score >= ?'
                params.append(criteria['min_mock_interview'])
            
            if 'min_internships' in criteria:
                base_query += ' AND pl.internships_completed >= ?'
                params.append(criteria['min_internships'])
            
            if 'programming_language' in criteria:
                base_query += ' AND p.language = ?'
                params.append(criteria['programming_language'])
            
            if 'placement_status' in criteria:
                base_query += ' AND pl.placement_status = ?'
                params.append(criteria['placement_status'])
            
            base_query += ' ORDER BY avg_soft_skills DESC, p.problems_solved DESC'
            
            return pd.read_sql_query(base_query, conn, params=params)

# Usage Example and Testing
if __name__ == "__main__":
    # Initialize database
    db = PlacementDatabase()
    
    # Generate sample data
    print("Generating sample data...")
    result = db.generate_sample_data(100)
    print(f"Generated data: {result}")
    
    # Test eligibility filtering
    criteria = {
        'min_problems_solved': 50,
        'min_soft_skills_avg': 75,
        'min_mock_interview': 70,
        'min_internships': 1
    }
    
    eligible_students = db.get_eligible_students(criteria)
    print(f"\nFound {len(eligible_students)} eligible students")
    print(eligible_students.head())
    
