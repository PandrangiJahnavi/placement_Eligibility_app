# 🎓 Placement Eligibility Streamlit Application

A comprehensive data-driven application built with Streamlit for managing student placement eligibility. This system helps placement teams filter and shortlist students based on customizable criteria, track performance metrics, and make data-driven decisions.

## 📋 Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Screenshots](#screenshots)
- [Key Functionality](#key-functionality)
- [SQL Queries](#sql-queries)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🔍 **Student Eligibility Filter**
- Interactive filtering based on programming performance
- Soft skills assessment criteria
- Mock interview score requirements
- Internship completion tracking
- Real-time results with download capability

### 📈 **Analytics Dashboard**
- Comprehensive placement metrics and KPIs
- Interactive visualizations using Plotly
- Performance distribution charts
- Top performer identification
- Placement trends analysis

### 👥 **Student Database Management**
- Complete student records view
- Advanced search and filtering
- Batch-wise student tracking
- Export functionality

### 🔧 **Database Management**
- Automated sample data generation using Faker
- Database statistics monitoring
- Sample SQL query examples

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python with Object-Oriented Programming
- **Database**: SQLite
- **Data Manipulation**: Pandas
- **Visualizations**: Plotly Express & Graph Objects
- **Data Generation**: Faker Library
- **Programming Language**: Python 3.8+

## 📁 Project Structure

```
placement_eligibility_app/
├── data_structures.py          # Core OOP classes and database management
├── streamlit_app.py            # Main Streamlit application
├── sql_queries.py              # 10 analytical SQL queries
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── placement_eligibility.db    # SQLite database (auto-generated)
└── placement_env/              # Virtual environment (optional)
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download the Project
```bash
# Create project directory
mkdir placement_eligibility_app
cd placement_eligibility_app
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv placement_env

# Activate virtual environment
# Windows:
placement_env\Scripts\activate
# Mac/Linux:
source placement_env/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install required packages
pip install streamlit faker pandas plotly
```

### Step 4: Create Project Files
Create the following files in your project directory:
- `data_structures.py` (Copy from provided code)
- `streamlit_app.py` (Copy from provided code)
- `requirements.txt`

## 🏃‍♂️ Usage

### Running the Application
```bash
# Start the Streamlit app
streamlit run streamlit_app.py
```

The application will automatically:
1. Create the SQLite database
2. Generate 100 sample student records
3. Open your browser to `http://localhost:8501`

### Navigation
- **🔍 Student Eligibility Filter**: Set criteria and find qualified students
- **📈 Analytics Dashboard**: View comprehensive insights and charts
- **👥 All Students**: Browse complete student database
- **🔧 Database Management**: Generate data and view statistics

## 🗃️ Database Schema

### Students Table
- `student_id` (Primary Key): Unique identifier
- `name`: Full name of the student
- `age`: Age of the student (18-35)
- `gender`: Gender (Male/Female/Other)
- `email`: Email address (unique)
- `phone`: Contact number
- `enrollment_year`: Year of enrollment
- `course_batch`: Batch/cohort identifier
- `city`: City of residence
- `graduation_year`: Expected graduation year

### Programming Table
- `programming_id` (Primary Key): Unique identifier
- `student_id` (Foreign Key): References students table
- `language`: Programming language (Python/SQL/Java/JavaScript)
- `problems_solved`: Number of coding problems solved
- `assessments_completed`: Completed assessments count
- `mini_projects`: Mini projects submitted
- `certifications_earned`: Programming certifications
- `latest_project_score`: Recent project score (0-100)

### Soft Skills Table
- `soft_skill_id` (Primary Key): Unique identifier
- `student_id` (Foreign Key): References students table
- `communication`: Communication skills score (0-100)
- `teamwork`: Teamwork skills score (0-100)
- `presentation`: Presentation skills score (0-100)
- `leadership`: Leadership skills score (0-100)
- `critical_thinking`: Critical thinking score (0-100)
- `interpersonal_skills`: Interpersonal skills score (0-100)

### Placements Table
- `placement_id` (Primary Key): Unique identifier
- `student_id` (Foreign Key): References students table
- `mock_interview_score`: Mock interview performance (0-100)
- `internships_completed`: Number of internships
- `placement_status`: Status (Ready/Not Ready/Placed)
- `company_name`: Placed company name (if applicable)
- `placement_package`: Salary package offered
- `interview_rounds_cleared`: Interview rounds cleared
- `placement_date`: Date of placement

## 📊 Key Functionality

### Eligibility Filtering
```python
# Example criteria
criteria = {
    'min_problems_solved': 50,
    'min_soft_skills_avg': 75,
    'min_mock_interview': 70,
    'min_internships': 1,
    'programming_language': 'Python'
}

eligible_students = db.get_eligible_students(criteria)
```

### Performance Calculation
- **Programming Score**: Weighted average of problems solved, assessments, projects, and certifications
- **Soft Skills Average**: Mean of all six soft skill categories
- **Placement Readiness**: Based on interview score and internship experience

## 🔍 SQL Queries

The application includes 10 analytical SQL queries for insights:

1. **Total Students by Batch**
2. **Average Programming Performance**
3. **Top 5 Students Ready for Placement**
4. **Soft Skills Distribution**
5. **Placement Rate by Programming Language**
6. **Students with High Interview Scores**
7. **Internship Completion Analysis**
8. **Company-wise Placement Distribution**
9. **Monthly Placement Trends**
10. **Student Performance Correlation**

## 🎯 Business Use Cases

1. **Placement Management**: Filter students based on company requirements
2. **Performance Tracking**: Monitor student progress across multiple metrics
3. **Data-Driven Decisions**: Use analytics for placement strategy
4. **Student Counseling**: Identify areas for improvement
5. **Batch Comparison**: Compare performance across different cohorts

## 🔧 Customization

### Adding New Criteria
Modify the `get_eligible_students()` method in `PlacementDatabase` class:

```python
# Add new filter criteria
if 'min_certifications' in criteria:
    base_query += ' AND p.certifications_earned >= ?'
    params.append(criteria['min_certifications'])
```

### Custom Data Generation
Adjust the `generate_sample_data()` method parameters:

```python
# Customize data ranges
age=self.fake.random_int(min=22, max=30),  # Custom age range
problems_solved=self.fake.random_int(min=20, max=200),  # Custom problem range
```

## 📈 Screenshots pdf

### Student Eligibility Filter
![Eligibility Filter](https://drive.google.com/file/d/1CgRJZiJ5l5ogqEK75v1uo0d7To9UG_FG/view?usp=drive_link)

### Analytics Dashboard
![Analytics Dashboard](https://drive.google.com/file/d/1bVFKpsNbBLrZg91genLmkZfzXbfGEj7R/view?usp=sharing)

### All Students View
![Students View](https://drive.google.com/file/d/1DJQ8wqnberXsohLJ-4oDlvyunoGcAiS4/view?usp=sharing)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 Project Evaluation Criteria

- ✅ **Functionality**: Dynamic filtering and data display
- ✅ **SQL Queries**: 10 comprehensive analytical queries
- ✅ **OOP Design**: Proper class implementation with validation
- ✅ **UI/UX**: Interactive Streamlit interface
- ✅ **Documentation**: Complete project documentation

## 🏷️ Technical Tags

`Streamlit` `Python` `OOP` `SQLite` `Faker` `Pandas` `Plotly` `Data Science` `Dashboard` `Analytics`

## 📞 Support

For questions or issues:
1. Check the troubleshooting section below
2. Review the code comments and documentation
3. Create an issue in the repository

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'streamlit'`
```bash
# Solution: Install missing packages
pip install streamlit faker pandas plotly
```

**Issue**: Database not found
```bash
# Solution: The database is auto-created on first run
python data_structures.py
```

**Issue**: PowerShell execution policy error
```bash
# Solution: Use Command Prompt instead of PowerShell
# Or run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📄 License

This project is created for educational purposes as part of the AIML course curriculum.

## 🙏 Acknowledgments

- **Faker Library**: For generating realistic sample data
- **Streamlit Team**: For the amazing framework
- **Plotly**: For interactive visualizations
- **Course Instructors**: For project guidance and requirements

---

**Built with ❤️ using Python and Streamlit**

*Last Updated: July 2025*


