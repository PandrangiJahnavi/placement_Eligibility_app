from data_structures import PlacementDatabase

# Initialize and test
db = PlacementDatabase()
print("Database created successfully!")

# Generate sample data
result = db.generate_sample_data(50)
print(f"Generated: {result}")

# Test filtering
criteria = {
    'min_problems_solved': 30,
    'min_soft_skills_avg': 60
}

eligible = db.get_eligible_students(criteria)
print(f"Found {len(eligible)} eligible students")