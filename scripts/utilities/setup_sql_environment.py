"""
SQL Practice Environment Setup
This script downloads the data_jobs dataset and creates a normalized database
for practicing SQL JOINs as described in Week 4 practice materials.
"""

import pandas as pd
import duckdb
from datasets import load_dataset
import os
from datetime import datetime

def setup_sql_environment():
    """
    Sets up the SQL practice environment by:
    1. Downloading the data_jobs dataset
    2. Creating normalized tables
    3. Setting up the database schema
    """
    
    print("🚀 Setting up SQL Practice Environment...")
    
    # Step 1: Download the dataset
    print("📥 Downloading data_jobs dataset...")
    try:
        ds = load_dataset("lukebarousse/data_jobs")
        df = ds['train'].to_pandas()
        print(f"✅ Downloaded {len(df):,} job records")
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return False
    
    # Step 2: Create DuckDB database
    print("🗄️  Creating DuckDB database...")
    
    # Create datasets directory if it doesn't exist
    import os
    os.makedirs('datasets', exist_ok=True)
    
    conn = duckdb.connect('datasets/data_jobs.db')
    
    # Step 3: Create normalized tables
    print("🔧 Creating normalized database schema...")
    
    # Create companies table
    companies_df = df[['company_name']].drop_duplicates().reset_index(drop=True)
    companies_df['company_id'] = companies_df.index + 1
    companies_df = companies_df[['company_id', 'company_name']]
    conn.execute("CREATE TABLE IF NOT EXISTS companies (company_id INTEGER PRIMARY KEY, company_name VARCHAR(255))")
    conn.execute("INSERT INTO companies SELECT * FROM companies_df")
    
    # Create locations table
    locations_df = df[['job_location', 'job_country']].drop_duplicates().reset_index(drop=True)
    locations_df['location_id'] = locations_df.index + 1
    locations_df = locations_df[['location_id', 'job_location', 'job_country']]
    conn.execute("CREATE TABLE IF NOT EXISTS locations (location_id INTEGER PRIMARY KEY, job_location VARCHAR(255), job_country VARCHAR(100))")
    conn.execute("INSERT INTO locations SELECT * FROM locations_df")
    
    # Create platforms table
    platforms_df = df[['job_via']].drop_duplicates().reset_index(drop=True)
    platforms_df.columns = ['platform_name']
    platforms_df['platform_id'] = platforms_df.index + 1
    platforms_df = platforms_df[['platform_id', 'platform_name']]
    conn.execute("CREATE TABLE IF NOT EXISTS platforms (platform_id INTEGER PRIMARY KEY, platform_name VARCHAR(255))")
    conn.execute("INSERT INTO platforms SELECT * FROM platforms_df")
    
    # Create jobs table with foreign keys
    jobs_df = df.copy()
    
    # Add foreign key mappings
    company_mapping = dict(zip(companies_df['company_name'], companies_df['company_id']))
    location_mapping = dict(zip(locations_df['job_location'], locations_df['location_id']))
    platform_mapping = dict(zip(platforms_df['platform_name'], platforms_df['platform_id']))
    
    jobs_df['company_id'] = jobs_df['company_name'].map(company_mapping)
    jobs_df['location_id'] = jobs_df['job_location'].map(location_mapping)
    jobs_df['platform_id'] = jobs_df['job_via'].map(platform_mapping)
    
    # Create job_id and select relevant columns
    jobs_df['job_id'] = jobs_df.index + 1
    jobs_final = jobs_df[[
        'job_id', 'company_id', 'location_id', 'platform_id',
        'job_title_short', 'job_title', 'job_schedule_type',
        'job_work_from_home', 'job_posted_date', 'job_no_degree_mention',
        'job_health_insurance', 'salary_rate', 'salary_year_avg', 'salary_hour_avg'
    ]]
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INTEGER PRIMARY KEY,
            company_id INTEGER,
            location_id INTEGER,
            platform_id INTEGER,
            job_title_short VARCHAR(100),
            job_title VARCHAR(255),
            job_schedule_type VARCHAR(50),
            job_work_from_home BOOLEAN,
            job_posted_date TIMESTAMP,
            job_no_degree_mention BOOLEAN,
            job_health_insurance BOOLEAN,
            salary_rate VARCHAR(20),
            salary_year_avg DECIMAL(10,2),
            salary_hour_avg DECIMAL(8,2)
        )
    """)
    conn.execute("INSERT INTO jobs SELECT * FROM jobs_final")
    
    # Create skills table (sample common skills)
    skills_data = [
        (1, 'Python', 'programming'),
        (2, 'SQL', 'programming'),
        (3, 'R', 'programming'),
        (4, 'Java', 'programming'),
        (5, 'JavaScript', 'programming'),
        (6, 'AWS', 'cloud'),
        (7, 'Azure', 'cloud'),
        (8, 'GCP', 'cloud'),
        (9, 'Tableau', 'analyst_tools'),
        (10, 'Power BI', 'analyst_tools'),
        (11, 'Excel', 'analyst_tools'),
        (12, 'Spark', 'big_data'),
        (13, 'Hadoop', 'big_data'),
        (14, 'Docker', 'devops'),
        (15, 'Kubernetes', 'devops')
    ]
    
    skills_df = pd.DataFrame(skills_data, columns=['skill_id', 'skill_name', 'skill_category'])
    conn.execute("CREATE TABLE IF NOT EXISTS skills (skill_id INTEGER PRIMARY KEY, skill_name VARCHAR(100), skill_category VARCHAR(50))")
    conn.execute("INSERT INTO skills SELECT * FROM skills_df")
    
    # Create job_skills table (sample relationships)
    # This creates realistic skill requirements for jobs
    import random
    random.seed(42)
    
    job_skills_data = []
    for job_id in range(1, min(10000, len(jobs_final) + 1)):  # Limit to first 10k jobs for demo
        # Each job has 2-5 skills
        num_skills = random.randint(2, 5)
        job_skills = random.sample(range(1, 16), num_skills)
        for skill_id in job_skills:
            job_skills_data.append((job_id, skill_id))
    
    job_skills_df = pd.DataFrame(job_skills_data, columns=['job_id', 'skill_id'])
    conn.execute("CREATE TABLE IF NOT EXISTS job_skills (job_id INTEGER, skill_id INTEGER, PRIMARY KEY (job_id, skill_id))")
    conn.execute("INSERT INTO job_skills SELECT * FROM job_skills_df")
    
    # Step 4: Create summary statistics
    print("📊 Database Summary:")
    print(f"   Companies: {len(companies_df):,}")
    print(f"   Locations: {len(locations_df):,}")
    print(f"   Platforms: {len(platforms_df):,}")
    print(f"   Jobs: {len(jobs_final):,}")
    print(f"   Skills: {len(skills_df):,}")
    print(f"   Job-Skill Relationships: {len(job_skills_df):,}")
    
    # Step 5: Test queries
    print("\n🧪 Testing database with sample queries...")
    
    # Test basic join
    result = conn.execute("""
        SELECT c.company_name, COUNT(j.job_id) as job_count
        FROM companies c
        INNER JOIN jobs j ON c.company_id = j.company_id
        GROUP BY c.company_name
        ORDER BY job_count DESC
        LIMIT 5
    """).fetchall()
    
    print("Top 5 companies by job count:")
    for row in result:
        print(f"   {row[0]}: {row[1]} jobs")
    
    conn.close()
    
    # Step 6: Register Jupyter kernel
    print("\n🔧 Registering Jupyter kernel...")
    try:
        import subprocess
        subprocess.run([
            'python', '-m', 'ipykernel', 'install', '--user', 
            '--name=sql-study-group', '--display-name=SQL Study Group'
        ], check=True, capture_output=True)
        print("✅ Jupyter kernel registered successfully!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Kernel registration failed: {e}")
        print("   You can register manually with:")
        print("   python -m ipykernel install --user --name=sql-study-group --display-name=\"SQL Study Group\"")
    except Exception as e:
        print(f"⚠️  Kernel registration error: {e}")
    
    print("\n✅ SQL Practice Environment Setup Complete!")
    print("📁 Database saved as: datasets/data_jobs.db")
    print("🎯 Ready for SQL practice!")
    
    return True

if __name__ == "__main__":
    setup_sql_environment() 