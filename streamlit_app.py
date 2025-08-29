import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_structures import PlacementDatabase, PlacementStatus, ProgrammingLanguage
import sqlite3

# Page configuration
st.set_page_config(
    page_title="Placement Eligibility System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def init_database():
    """Initialize database and generate sample data if needed"""
    db = PlacementDatabase()
    
    # Check if database has data
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Generate sample data if database is empty
            with st.spinner("Generating sample data... This will take a moment."):
                db.generate_sample_data(100)
    
    return db

# Load database
db = init_database()

# App title and description
st.title("🎓 Placement Eligibility System")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["🔍 Student Eligibility Filter", "📈 Analytics Dashboard", "👥 All Students", "🔧 Database Management"]
)

if page == "🔍 Student Eligibility Filter":
    st.header("🔍 Filter Eligible Students")
    st.markdown("Set your criteria to find students who meet placement requirements.")
    
    # Create two columns for criteria input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💻 Programming Criteria")
        min_problems = st.slider("Minimum Problems Solved", 0, 200, 50)
        min_assessments = st.slider("Minimum Assessments Completed", 0, 30, 10)
        min_projects = st.slider("Minimum Mini Projects", 0, 15, 3)
        programming_language = st.selectbox(
            "Programming Language", 
            ["Any"] + [lang.value for lang in ProgrammingLanguage]
        )
    
    with col2:
        st.subheader("🤝 Soft Skills & Placement Criteria")
        min_soft_skills = st.slider("Minimum Average Soft Skills Score", 0, 100, 70)
        min_mock_interview = st.slider("Minimum Mock Interview Score", 0, 100, 60)
        min_internships = st.slider("Minimum Internships Completed", 0, 5, 1)
        placement_status_filter = st.selectbox(
            "Placement Status",
            ["Any", "Ready", "Not Ready", "Placed"]
        )
    
    # Build criteria dictionary
    criteria = {
        'min_problems_solved': min_problems,
        'min_soft_skills_avg': min_soft_skills,
        'min_mock_interview': min_mock_interview,
        'min_internships': min_internships
    }
    
    if min_assessments > 0:
        criteria['min_assessments'] = min_assessments
    
    if min_projects > 0:
        criteria['min_projects'] = min_projects
    
    if programming_language != "Any":
        criteria['programming_language'] = programming_language
        
    if placement_status_filter != "Any":
        criteria['placement_status'] = placement_status_filter
    
    # Filter button
    if st.button("🔍 Find Eligible Students", type="primary"):
        with st.spinner("Searching for eligible students..."):
            eligible_students = db.get_eligible_students(criteria)
            
            if len(eligible_students) > 0:
                st.success(f"✅ Found {len(eligible_students)} eligible students!")
                
                # Display summary metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Students", len(eligible_students))
                with col2:
                    st.metric("Avg Problems Solved", f"{eligible_students['problems_solved'].mean():.0f}")
                with col3:
                    st.metric("Avg Soft Skills", f"{eligible_students['avg_soft_skills'].mean():.1f}")
                with col4:
                    placed_count = len(eligible_students[eligible_students['placement_status'] == 'Placed'])
                    st.metric("Already Placed", placed_count)
                
                # Display detailed results
                st.subheader("📋 Eligible Students Details")
                
                # Format the dataframe for better display
                display_df = eligible_students.copy()
                display_df['avg_soft_skills'] = display_df['avg_soft_skills'].round(1)
                display_df['mock_interview_score'] = display_df['mock_interview_score'].round(1)
                display_df['latest_project_score'] = display_df['latest_project_score'].round(1)
                
                # Reorder columns for better readability
                column_order = ['name', 'course_batch', 'language', 'problems_solved', 
                               'avg_soft_skills', 'mock_interview_score', 'internships_completed',
                               'placement_status', 'company_name', 'email']
                display_df = display_df[column_order]
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download button
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Eligible Students CSV",
                    data=csv,
                    file_name="eligible_students.csv",
                    mime="text/csv"
                )
                
            else:
                st.warning("❌ No students found matching the specified criteria. Try adjusting your filters.")

elif page == "📈 Analytics Dashboard":
    st.header("📈 Analytics Dashboard")
    st.markdown("Comprehensive insights into student performance and placement trends.")
    
    # Load all data for analytics
    with sqlite3.connect(db.db_path) as conn:
        # Get comprehensive data
        query = """
        SELECT 
            s.student_id, s.name, s.age, s.course_batch, s.city, s.enrollment_year,
            p.language, p.problems_solved, p.assessments_completed, p.mini_projects,
            p.certifications_earned, p.latest_project_score,
            (ss.communication + ss.teamwork + ss.presentation + 
             ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6 as avg_soft_skills,
            ss.communication, ss.teamwork, ss.presentation, ss.leadership, 
            ss.critical_thinking, ss.interpersonal_skills,
            pl.mock_interview_score, pl.internships_completed, pl.placement_status,
            pl.company_name, pl.placement_package
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        JOIN placements pl ON s.student_id = pl.student_id
        """
        all_data = pd.read_sql_query(query, conn)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(all_data)
        st.metric("📚 Total Students", total_students)
    
    with col2:
        placed_students = len(all_data[all_data['placement_status'] == 'Placed'])
        placement_rate = (placed_students / total_students) * 100
        st.metric("🎯 Placement Rate", f"{placement_rate:.1f}%")
    
    with col3:
        avg_package = all_data[all_data['placement_package'].notna()]['placement_package'].mean()
        st.metric("💰 Avg Package", f"${avg_package:,.0f}" if pd.notna(avg_package) else "N/A")
    
    with col4:
        ready_students = len(all_data[all_data['placement_status'] == 'Ready'])
        st.metric("✅ Ready for Placement", ready_students)
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Problems Solved Distribution")
        fig_problems = px.histogram(
            all_data, 
            x='problems_solved', 
            nbins=20,
            title="Distribution of Problems Solved",
            color_discrete_sequence=['#1f77b4']
        )
        fig_problems.update_layout(height=400)
        st.plotly_chart(fig_problems, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Placement Status Overview")
        status_counts = all_data['placement_status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Student Placement Status"
        )
        fig_status.update_layout(height=400)
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Soft Skills vs Mock Interview Performance")
        fig_scatter = px.scatter(
            all_data,
            x='avg_soft_skills',
            y='mock_interview_score',
            color='placement_status',
            size='problems_solved',
            hover_data=['name', 'course_batch'],
            title="Soft Skills vs Interview Performance"
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.subheader("💻 Programming Language Distribution")
        lang_counts = all_data['language'].value_counts()
        fig_lang = px.bar(
            x=lang_counts.index,
            y=lang_counts.values,
            title="Students by Programming Language",
            color=lang_counts.values,
            color_continuous_scale='viridis'
        )
        fig_lang.update_layout(height=400)
        st.plotly_chart(fig_lang, use_container_width=True)
    
    # Top Performers Section
    st.markdown("---")
    st.subheader("🏆 Top Performers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Top 5 Problem Solvers**")
        top_problems = all_data.nlargest(5, 'problems_solved')[['name', 'problems_solved', 'course_batch']]
        st.dataframe(top_problems, hide_index=True)
    
    with col2:
        st.write("**Highest Soft Skills Scores**")
        top_soft = all_data.nlargest(5, 'avg_soft_skills')[['name', 'avg_soft_skills', 'course_batch']]
        top_soft['avg_soft_skills'] = top_soft['avg_soft_skills'].round(1)
        st.dataframe(top_soft, hide_index=True)
    
    with col3:
        st.write("**Best Interview Performers**")
        top_interview = all_data.nlargest(5, 'mock_interview_score')[['name', 'mock_interview_score', 'course_batch']]
        top_interview['mock_interview_score'] = top_interview['mock_interview_score'].round(1)
        st.dataframe(top_interview, hide_index=True)

elif page == "👥 All Students":
    st.header("👥 All Students Database")
    st.markdown("Complete view of all students in the system.")
    
    # Load all student data
    with sqlite3.connect(db.db_path) as conn:
        query = """
        SELECT 
            s.student_id, s.name, s.age, s.email, s.course_batch, s.city,
            p.language, p.problems_solved, p.mini_projects,
            (ss.communication + ss.teamwork + ss.presentation + 
             ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6 as avg_soft_skills,
            pl.mock_interview_score, pl.placement_status, pl.company_name
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        JOIN placements pl ON s.student_id = pl.student_id
        ORDER BY s.name
        """
        all_students = pd.read_sql_query(query, conn)
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_name = st.text_input("🔍 Search by Name")
    
    with col2:
        batch_filter = st.selectbox(
            "Filter by Batch",
            ["All"] + sorted(all_students['course_batch'].unique().tolist())
        )
    
    with col3:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All"] + sorted(all_students['placement_status'].unique().tolist())
        )
    
    # Apply filters
    filtered_data = all_students.copy()
    
    if search_name:
        filtered_data = filtered_data[filtered_data['name'].str.contains(search_name, case=False, na=False)]
    
    if batch_filter != "All":
        filtered_data = filtered_data[filtered_data['course_batch'] == batch_filter]
    
    if status_filter != "All":
        filtered_data = filtered_data[filtered_data['placement_status'] == status_filter]
    
    st.success(f"Showing {len(filtered_data)} of {len(all_students)} students")
    
    # Format data for display
    display_data = filtered_data.copy()
    display_data['avg_soft_skills'] = display_data['avg_soft_skills'].round(1)
    display_data['mock_interview_score'] = display_data['mock_interview_score'].round(1)
    
    # Display table
    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
    
    # Download filtered data
    csv = display_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Student Data CSV",
        data=csv,
        file_name="students_data.csv",
        mime="text/csv"
    )

elif page == "🔧 Database Management":
    st.header("🔧 Database Management")
    st.markdown("Manage your database and generate new sample data.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Database Statistics")
        
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            # Get table counts
            tables = ['students', 'programming', 'soft_skills', 'placements']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                st.metric(f"{table.title()} Records", count)
    
    with col2:
        st.subheader("⚡ Actions")
        
        # Generate new data
        num_students = st.number_input("Number of students to generate", min_value=10, max_value=500, value=50)
        
        if st.button("🔄 Generate New Sample Data", type="primary"):
            with st.spinner(f"Generating {num_students} student records..."):
                result = db.generate_sample_data(num_students)
                st.success(f"✅ Generated {result['students']} new student records!")
                st.balloons()
        
        st.markdown("---")
        
        # Database info
        st.subheader("📋 Database Information")
        st.info(f"Database Location: `{db.db_path}`")
        
        # Show sample queries
        st.subheader("🔍 Sample SQL Queries")
        
        sample_queries = [
            "SELECT COUNT(*) as total_students FROM students;",
            "SELECT placement_status, COUNT(*) as count FROM placements GROUP BY placement_status;",
            "SELECT AVG(problems_solved) as avg_problems FROM programming;",
            "SELECT name, problems_solved FROM students s JOIN programming p ON s.student_id = p.student_id ORDER BY problems_solved DESC LIMIT 5;"
        ]
        
        for i, query in enumerate(sample_queries, 1):
            st.code(query, language="sql")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🎓 Placement Eligibility System | Built with Streamlit & Python OOP</p>
    </div>
    """, 
    unsafe_allow_html=True
)
