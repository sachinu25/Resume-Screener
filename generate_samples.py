"""
generate_samples.py - Generate sample PDF resumes for testing
Run this once to create test resumes in the resumes/ folder

Usage: python generate_samples.py
"""

import os

# We'll use a simple approach to create PDFs using reportlab-like text
# But since we want minimal dependencies, let's use fpdf approach
# Actually, let's just create them as text and convert - simplest approach

# For testing, we'll create resumes using pdfplumber's sister library
# But to keep it simple, let's use a built-in approach

def create_sample_resumes():
    """Create sample resume text files that can be tested."""

    resumes = {
        "John_Doe_Resume.txt": """John Doe
Email: john.doe@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

SUMMARY
Full Stack Software Engineer with 3+ years of experience building scalable web applications. 
Proficient in Python, JavaScript, and cloud technologies. Passionate about clean code and 
agile development practices.

EDUCATION
Bachelor of Science in Computer Science
State University, 2020
GPA: 3.7/4.0

EXPERIENCE
Software Engineer | TechCorp Inc. | Jan 2021 - Present
- Developed RESTful APIs using Python Flask and Django frameworks
- Built responsive front-end interfaces with React and JavaScript
- Managed MySQL and PostgreSQL databases for production applications
- Implemented CI/CD pipelines using Jenkins and Docker
- Collaborated in Agile/Scrum team of 8 developers
- Reduced API response time by 40% through query optimization

Junior Developer | WebStart Solutions | Jun 2020 - Dec 2020
- Created web applications using HTML, CSS, JavaScript and Bootstrap
- Assisted in database design and SQL query writing
- Participated in code reviews and testing
- Worked with Git version control for team collaboration

SKILLS
Programming: Python, JavaScript, Java, SQL, HTML, CSS
Frameworks: Flask, Django, React, Node.js, Bootstrap
Databases: MySQL, PostgreSQL, MongoDB
Tools: Git, Docker, Jenkins, AWS, Linux, Jira
Other: REST API, Agile, Scrum, Unit Testing, CI/CD

PROJECTS
E-commerce Platform | Python, Django, PostgreSQL
- Built a full-stack e-commerce site with payment integration
- Implemented user authentication and product catalog management

Task Management App | React, Node.js, MongoDB
- Developed a real-time task tracking application
- Used WebSockets for live updates between team members

CERTIFICATIONS
- AWS Cloud Practitioner (2022)
- Python Professional Certificate - Coursera (2021)
""",

        "Rahul_Sharma_Resume.txt": """Rahul Sharma
rahul.sharma@gmail.com | +91-9876543210
Portfolio: rahulsharma.dev

OBJECTIVE
Aspiring Data Scientist with strong foundation in machine learning, statistics, and data analysis.
Looking for opportunities to apply analytical skills to solve real-world business problems.

EDUCATION
B.Tech in Information Technology
Indian Institute of Technology, 2022
CGPA: 8.5/10

TECHNICAL SKILLS
Languages: Python, R, SQL, Java
ML/AI: Scikit-learn, Pandas, NumPy, Matplotlib, NLP, Machine Learning, Data Science
Data: MySQL, MongoDB, Tableau, Power BI, Excel, Data Analysis, Data Visualization
Tools: Git, Jupyter, Google Colab, Linux, Docker
Concepts: Statistics, Feature Engineering, Deep Learning basics, Natural Language Processing

EXPERIENCE
Data Science Intern | Analytics Hub Pvt. Ltd. | May 2022 - Nov 2022
- Built predictive models using Python and Scikit-learn for customer churn prediction
- Performed exploratory data analysis on datasets with 500K+ records using Pandas
- Created interactive dashboards using Tableau for business stakeholders
- Applied NLP techniques for sentiment analysis of customer reviews
- Improved model accuracy by 15% through feature engineering

Research Assistant | IIT ML Lab | Jan 2022 - Apr 2022
- Assisted in research on natural language processing applications
- Implemented text classification models using machine learning
- Analyzed large text datasets and created data visualization reports

PROJECTS
Movie Recommendation System | Python, Scikit-learn, Flask
- Built collaborative filtering based recommendation engine
- Deployed as web application using Flask

Sentiment Analysis Tool | Python, NLTK, Machine Learning
- Developed text classification model for tweet sentiment analysis
- Achieved 87% accuracy using TF-IDF and SVM classifier

Sales Forecasting Dashboard | Python, Pandas, Tableau
- Created time series forecasting model for retail sales data
- Built interactive Tableau dashboard for visualization

CERTIFICATIONS
- Machine Learning Specialization - Andrew Ng (Coursera)
- Data Science Professional Certificate - IBM
""",

        "Sarah_Chen_Resume.txt": """Sarah Chen
sarah.chen@outlook.com
(555) 987-6543 | San Francisco, CA

PROFESSIONAL SUMMARY
Senior Software Engineer with 5 years of experience specializing in cloud architecture 
and backend development. Strong expertise in Python, AWS, and distributed systems. 
Proven track record of leading engineering teams and delivering high-impact projects.

EDUCATION
Master of Science in Computer Science
Stanford University, 2019

Bachelor of Science in Software Engineering
UC Berkeley, 2017

WORK EXPERIENCE
Senior Software Engineer | CloudTech Solutions | Mar 2021 - Present
- Architected microservices infrastructure on AWS serving 2M+ daily users
- Led team of 5 engineers in redesigning the core API platform
- Implemented auto-scaling solutions using Kubernetes and Docker
- Built data pipelines using Python, Apache Spark, and Kafka
- Established CI/CD workflows with Jenkins and Terraform
- Mentored 3 junior developers in software engineering best practices

Software Engineer | DataFlow Inc. | Jul 2019 - Feb 2021
- Developed Python backend services using Django and FastAPI
- Designed and optimized PostgreSQL database schemas
- Built RESTful and GraphQL APIs for mobile and web clients
- Integrated AWS services (S3, Lambda, SQS, DynamoDB) for scalable solutions
- Implemented automated testing achieving 90% code coverage

Software Engineering Intern | Google | Summer 2018
- Contributed to internal tooling for code review automation
- Built a monitoring dashboard using JavaScript and React

TECHNICAL SKILLS
Languages: Python, Java, Go, JavaScript, TypeScript, SQL, Bash
Backend: Django, FastAPI, Flask, Spring, Node.js, Express
Cloud & DevOps: AWS, GCP, Docker, Kubernetes, Terraform, Jenkins, CI/CD
Databases: PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, Elasticsearch
Big Data: Apache Spark, Hadoop, Kafka
Other: Microservices, REST, GraphQL, Git, Linux, Agile, Scrum, Leadership, Project Management

PUBLICATIONS
- "Optimizing Distributed Cache Systems" - IEEE Conference 2021
""",

        "Mike_Johnson_Resume.txt": """Mike Johnson
mike.j@email.com | (555) 456-7890

ABOUT ME
Recent Computer Science graduate eager to start career in software development.
Quick learner with good programming fundamentals and teamwork skills.

EDUCATION
Bachelor of Science in Computer Science
Community College of Technology, 2023
GPA: 3.2/4.0

COURSEWORK
Data Structures, Algorithms, Database Systems, Web Development, 
Operating Systems, Computer Networks

SKILLS
Languages: Python, Java, HTML, CSS, JavaScript
Databases: MySQL, SQLite
Tools: Git, VS Code
Concepts: Object-Oriented Programming, Basic SQL

PROJECTS
Personal Blog Website | HTML, CSS, JavaScript
- Created a responsive personal blog using Bootstrap
- Implemented basic CRUD operations with local storage

Calculator App | Java
- Built a GUI calculator application using Java Swing
- Handles basic arithmetic operations

Student Database | Python, SQLite
- Simple CRUD application for managing student records
- Used Python with SQLite for data storage

EXTRACURRICULAR
- Member, Computer Science Club (2021-2023)
- Volunteer, Code for Kids workshop
- Hackathon participant - 2022 College Hackfest

REFERENCES
Available upon request
""",

        "Priya_Patel_Resume.txt": """Priya Patel
priya.patel@protonmail.com | +91-8765432109
LinkedIn: linkedin.com/in/priyapatel

SUMMARY
DevOps Engineer with 2 years of hands-on experience in cloud infrastructure, 
automation, and CI/CD pipeline management. AWS certified professional with 
strong scripting skills in Python and Bash.

EDUCATION
B.E. in Computer Science and Engineering
PES University, Bangalore, 2021
CGPA: 8.2/10

EXPERIENCE
DevOps Engineer | InfraOps Technologies | Aug 2021 - Present
- Managed AWS cloud infrastructure including EC2, S3, RDS, and Lambda
- Built and maintained CI/CD pipelines using Jenkins, GitHub Actions
- Containerized applications using Docker and orchestrated with Kubernetes
- Wrote automation scripts in Python and Bash for deployment workflows
- Implemented Infrastructure as Code using Terraform and Ansible
- Configured monitoring using Prometheus and Grafana
- Managed Linux servers and Nginx web server configurations
- Reduced deployment time by 60% through pipeline optimization

TECHNICAL SKILLS
Cloud: AWS (EC2, S3, RDS, Lambda, CloudFormation), Azure basics
DevOps: Docker, Kubernetes, Jenkins, Terraform, Ansible, CI/CD
Scripting: Python, Bash, Shell scripting
Monitoring: Prometheus, Grafana, CloudWatch
OS: Linux (Ubuntu, CentOS), Windows Server
VCS: Git, GitHub, GitLab
Networking: TCP/IP, DNS, Load Balancing, Nginx
Databases: MySQL, PostgreSQL, Redis
Other: Agile, Jira, Confluence, Automation, Cybersecurity basics

CERTIFICATIONS
- AWS Solutions Architect Associate (2022)
- Docker Certified Associate (2023)
- Linux Foundation Certified System Administrator

PROJECTS
Automated Deployment Pipeline
- Built end-to-end CI/CD pipeline for microservices architecture
- Technologies: Jenkins, Docker, Kubernetes, Terraform

Server Monitoring Dashboard
- Created real-time monitoring system for 50+ servers
- Technologies: Python, Prometheus, Grafana
"""
    }

    print("Sample resume content generated!")
    print("\nTo test the system, you'll need actual PDF resumes.")
    print("You can:")
    print("  1. Convert these text files to PDF using any online tool")
    print("  2. Use your own resume PDFs")
    print("  3. Create PDFs from these templates using Google Docs or Word")
    print()

    # Save as text files for reference
    sample_dir = os.path.join('dataset', 'sample_resumes_text')
    os.makedirs(sample_dir, exist_ok=True)

    for filename, content in resumes.items():
        filepath = os.path.join(sample_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Saved: {filepath}")

    # Also save a sample job description
    sample_jd = """Software Engineer - Full Stack Development

We are looking for a skilled Software Engineer to join our development team. The ideal candidate 
should have strong experience in full-stack web development.

Requirements:
- 2+ years of experience in software development
- Proficiency in Python and JavaScript
- Experience with web frameworks like Django, Flask, or React
- Knowledge of SQL databases (MySQL, PostgreSQL)
- Familiarity with Git version control and CI/CD pipelines
- Understanding of RESTful API design
- Experience with cloud services (AWS or Azure)
- Strong problem-solving and communication skills

Nice to have:
- Experience with Docker and Kubernetes
- Knowledge of machine learning basics
- Familiarity with Agile/Scrum methodologies
- Experience with data analysis using Pandas or NumPy

Education: Bachelor's degree in Computer Science or related field"""

    jd_path = os.path.join('dataset', 'sample_job_description.txt')
    with open(jd_path, 'w', encoding='utf-8') as f:
        f.write(sample_jd)
    print(f"\n  Saved: {jd_path}")

    print("\nDone! Check the dataset/ folder for sample content.")


if __name__ == '__main__':
    create_sample_resumes()
