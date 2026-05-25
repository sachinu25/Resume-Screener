"""
create_pdf_resumes.py - Generate actual PDF resumes for testing
Uses fpdf2 library to create proper PDF files from sample data

Usage: pip install fpdf2 && python create_pdf_resumes.py
"""

import os
import sys

try:
    from fpdf import FPDF
except ImportError:
    print("fpdf2 not installed. Installing...")
    os.system(f"{sys.executable} -m pip install fpdf2")
    from fpdf import FPDF


class ResumePDF(FPDF):
    """Custom PDF class for generating resume documents."""

    def header(self):
        pass  # No automatic header

    def section_title(self, title):
        self.set_x(10)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(30, 30, 30)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(79, 70, 229)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def add_text(self, text, bold=False, size=10):
        self.set_x(10)
        self.set_font('Helvetica', 'B' if bold else '', size)
        self.set_text_color(50, 50, 50)
        self.multi_cell(190, 5, text)
        self.ln(1)

    def add_bullet(self, text):
        self.set_x(15)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(60, 60, 60)
        self.multi_cell(185, 5, f"- {text}")


def create_john_doe():
    pdf = ResumePDF()
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, 'John Doe', new_x="LMARGIN", new_y="NEXT", align='C')

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe | github.com/johndoe',
             new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    pdf.section_title('SUMMARY')
    pdf.add_text('Full Stack Software Engineer with 3+ years of experience building scalable web applications. '
                 'Proficient in Python, JavaScript, and cloud technologies. Passionate about clean code and agile development.')

    pdf.section_title('EXPERIENCE')
    pdf.add_text('Software Engineer | TechCorp Inc. | Jan 2021 - Present', bold=True)
    pdf.add_bullet('Developed RESTful APIs using Python Flask and Django frameworks')
    pdf.add_bullet('Built responsive front-end interfaces with React and JavaScript')
    pdf.add_bullet('Managed MySQL and PostgreSQL databases for production applications')
    pdf.add_bullet('Implemented CI/CD pipelines using Jenkins and Docker')
    pdf.add_bullet('Collaborated in Agile/Scrum team of 8 developers')
    pdf.add_bullet('Reduced API response time by 40% through query optimization')
    pdf.ln(2)

    pdf.add_text('Junior Developer | WebStart Solutions | Jun 2020 - Dec 2020', bold=True)
    pdf.add_bullet('Created web applications using HTML, CSS, JavaScript and Bootstrap')
    pdf.add_bullet('Worked with Git version control for team collaboration')
    pdf.add_bullet('Participated in code reviews and testing')
    pdf.ln(2)

    pdf.section_title('EDUCATION')
    pdf.add_text('B.Sc. Computer Science | State University | 2020 | GPA: 3.7/4.0', bold=True)

    pdf.section_title('SKILLS')
    pdf.add_text('Programming: Python, JavaScript, Java, SQL, HTML, CSS')
    pdf.add_text('Frameworks: Flask, Django, React, Node.js, Bootstrap')
    pdf.add_text('Tools: Git, Docker, Jenkins, AWS, Linux, MySQL, PostgreSQL, MongoDB')
    pdf.add_text('Other: REST API, Agile, Scrum, Unit Testing, CI/CD')

    pdf.section_title('CERTIFICATIONS')
    pdf.add_bullet('AWS Cloud Practitioner (2022)')
    pdf.add_bullet('Python Professional Certificate - Coursera (2021)')

    return pdf


def create_rahul_sharma():
    pdf = ResumePDF()
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, 'Rahul Sharma', new_x="LMARGIN", new_y="NEXT", align='C')

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'rahul.sharma@gmail.com | +91-9876543210 | rahulsharma.dev',
             new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    pdf.section_title('OBJECTIVE')
    pdf.add_text('Aspiring Data Scientist with strong foundation in machine learning, statistics, and data analysis. '
                 'Looking for opportunities to apply analytical skills to solve real-world problems.')

    pdf.section_title('EXPERIENCE')
    pdf.add_text('Data Science Intern | Analytics Hub Pvt. Ltd. | May 2022 - Nov 2022', bold=True)
    pdf.add_bullet('Built predictive models using Python and Scikit-learn for customer churn prediction')
    pdf.add_bullet('Performed exploratory data analysis on 500K+ records using Pandas')
    pdf.add_bullet('Created interactive dashboards using Tableau for business stakeholders')
    pdf.add_bullet('Applied NLP techniques for sentiment analysis of customer reviews')
    pdf.add_bullet('Improved model accuracy by 15% through feature engineering')
    pdf.ln(2)

    pdf.add_text('Research Assistant | IIT ML Lab | Jan 2022 - Apr 2022', bold=True)
    pdf.add_bullet('Assisted in research on natural language processing applications')
    pdf.add_bullet('Implemented text classification models using machine learning')
    pdf.ln(2)

    pdf.section_title('EDUCATION')
    pdf.add_text('B.Tech Information Technology | Indian Institute of Technology | 2022 | CGPA: 8.5/10', bold=True)

    pdf.section_title('SKILLS')
    pdf.add_text('Languages: Python, R, SQL, Java')
    pdf.add_text('ML/AI: Scikit-learn, Pandas, NumPy, Matplotlib, NLP, Machine Learning, Data Science')
    pdf.add_text('Data: MySQL, MongoDB, Tableau, Power BI, Excel, Data Analysis, Data Visualization')
    pdf.add_text('Tools: Git, Docker, Linux, Statistics, Feature Engineering')

    pdf.section_title('PROJECTS')
    pdf.add_text('Movie Recommendation System | Python, Scikit-learn, Flask', bold=True)
    pdf.add_bullet('Built collaborative filtering recommendation engine deployed with Flask')
    pdf.ln(1)
    pdf.add_text('Sentiment Analysis Tool | Python, NLTK, ML', bold=True)
    pdf.add_bullet('Text classification model with 87% accuracy using TF-IDF and SVM')

    pdf.section_title('CERTIFICATIONS')
    pdf.add_bullet('Machine Learning Specialization - Andrew Ng (Coursera)')
    pdf.add_bullet('Data Science Professional Certificate - IBM')

    return pdf


def create_sarah_chen():
    pdf = ResumePDF()
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, 'Sarah Chen', new_x="LMARGIN", new_y="NEXT", align='C')

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'sarah.chen@outlook.com | (555) 987-6543 | San Francisco, CA',
             new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    pdf.section_title('PROFESSIONAL SUMMARY')
    pdf.add_text('Senior Software Engineer with 5 years of experience specializing in cloud architecture '
                 'and backend development. Strong expertise in Python, AWS, and distributed systems.')

    pdf.section_title('EXPERIENCE')
    pdf.add_text('Senior Software Engineer | CloudTech Solutions | Mar 2021 - Present', bold=True)
    pdf.add_bullet('Architected microservices infrastructure on AWS serving 2M+ daily users')
    pdf.add_bullet('Led team of 5 engineers in redesigning the core API platform')
    pdf.add_bullet('Implemented auto-scaling with Kubernetes and Docker')
    pdf.add_bullet('Built data pipelines using Python, Apache Spark, and Kafka')
    pdf.add_bullet('Established CI/CD workflows with Jenkins and Terraform')
    pdf.ln(2)

    pdf.add_text('Software Engineer | DataFlow Inc. | Jul 2019 - Feb 2021', bold=True)
    pdf.add_bullet('Developed Python backend services using Django and FastAPI')
    pdf.add_bullet('Built RESTful and GraphQL APIs for mobile and web clients')
    pdf.add_bullet('Integrated AWS services (S3, Lambda, DynamoDB) for scalable solutions')
    pdf.add_bullet('Implemented automated testing achieving 90% code coverage')
    pdf.ln(2)

    pdf.section_title('EDUCATION')
    pdf.add_text('M.S. Computer Science | Stanford University | 2019', bold=True)
    pdf.add_text('B.S. Software Engineering | UC Berkeley | 2017', bold=True)

    pdf.section_title('SKILLS')
    pdf.add_text('Languages: Python, Java, Go, JavaScript, TypeScript, SQL, Bash')
    pdf.add_text('Backend: Django, FastAPI, Flask, Spring, Node.js, Express')
    pdf.add_text('Cloud/DevOps: AWS, GCP, Docker, Kubernetes, Terraform, Jenkins, CI/CD')
    pdf.add_text('Databases: PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, Elasticsearch')
    pdf.add_text('Other: Microservices, REST, GraphQL, Git, Linux, Agile, Scrum, Leadership')

    return pdf


def create_mike_johnson():
    pdf = ResumePDF()
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, 'Mike Johnson', new_x="LMARGIN", new_y="NEXT", align='C')

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'mike.j@email.com | (555) 456-7890',
             new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    pdf.section_title('ABOUT ME')
    pdf.add_text('Recent Computer Science graduate eager to start career in software development. '
                 'Quick learner with good programming fundamentals and teamwork skills.')

    pdf.section_title('EDUCATION')
    pdf.add_text('B.Sc. Computer Science | Community College of Technology | 2023 | GPA: 3.2/4.0', bold=True)
    pdf.add_text('Coursework: Data Structures, Algorithms, Database Systems, Web Development')

    pdf.section_title('SKILLS')
    pdf.add_text('Languages: Python, Java, HTML, CSS, JavaScript')
    pdf.add_text('Databases: MySQL, SQLite')
    pdf.add_text('Tools: Git, VS Code')

    pdf.section_title('PROJECTS')
    pdf.add_text('Personal Blog Website | HTML, CSS, JavaScript', bold=True)
    pdf.add_bullet('Created a responsive personal blog using Bootstrap')
    pdf.add_bullet('Implemented basic CRUD operations with local storage')
    pdf.ln(1)
    pdf.add_text('Calculator App | Java', bold=True)
    pdf.add_bullet('Built a GUI calculator application using Java Swing')
    pdf.ln(1)
    pdf.add_text('Student Database | Python, SQLite', bold=True)
    pdf.add_bullet('Simple CRUD application for managing student records')

    pdf.section_title('EXTRACURRICULAR')
    pdf.add_bullet('Member, Computer Science Club (2021-2023)')
    pdf.add_bullet('Volunteer, Code for Kids workshop')
    pdf.add_bullet('Hackathon participant - 2022 College Hackfest')

    return pdf


def create_priya_patel():
    pdf = ResumePDF()
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, 'Priya Patel', new_x="LMARGIN", new_y="NEXT", align='C')

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'priya.patel@protonmail.com | +91-8765432109 | linkedin.com/in/priyapatel',
             new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    pdf.section_title('SUMMARY')
    pdf.add_text('DevOps Engineer with 2 years of hands-on experience in cloud infrastructure, '
                 'automation, and CI/CD pipeline management. AWS certified professional.')

    pdf.section_title('EXPERIENCE')
    pdf.add_text('DevOps Engineer | InfraOps Technologies | Aug 2021 - Present', bold=True)
    pdf.add_bullet('Managed AWS cloud infrastructure including EC2, S3, RDS, and Lambda')
    pdf.add_bullet('Built and maintained CI/CD pipelines using Jenkins, GitHub Actions')
    pdf.add_bullet('Containerized applications using Docker and orchestrated with Kubernetes')
    pdf.add_bullet('Wrote automation scripts in Python and Bash for deployment')
    pdf.add_bullet('Implemented Infrastructure as Code using Terraform and Ansible')
    pdf.add_bullet('Reduced deployment time by 60% through pipeline optimization')
    pdf.ln(2)

    pdf.section_title('EDUCATION')
    pdf.add_text('B.E. Computer Science | PES University, Bangalore | 2021 | CGPA: 8.2/10', bold=True)

    pdf.section_title('SKILLS')
    pdf.add_text('Cloud: AWS (EC2, S3, RDS, Lambda), Azure basics')
    pdf.add_text('DevOps: Docker, Kubernetes, Jenkins, Terraform, Ansible, CI/CD')
    pdf.add_text('Scripting: Python, Bash, Shell scripting')
    pdf.add_text('Databases: MySQL, PostgreSQL, Redis')
    pdf.add_text('Other: Git, GitHub, GitLab, Linux, Nginx, Agile, Jira, Cybersecurity')

    pdf.section_title('CERTIFICATIONS')
    pdf.add_bullet('AWS Solutions Architect Associate (2022)')
    pdf.add_bullet('Docker Certified Associate (2023)')
    pdf.add_bullet('Linux Foundation Certified System Administrator')

    return pdf


def main():
    output_dir = os.path.join('dataset', 'sample_resumes')
    os.makedirs(output_dir, exist_ok=True)

    resumes = {
        'John_Doe_Resume.pdf': create_john_doe,
        'Rahul_Sharma_Resume.pdf': create_rahul_sharma,
        'Sarah_Chen_Resume.pdf': create_sarah_chen,
        'Mike_Johnson_Resume.pdf': create_mike_johnson,
        'Priya_Patel_Resume.pdf': create_priya_patel,
    }

    print("Generating sample PDF resumes...\n")

    for filename, creator_fn in resumes.items():
        filepath = os.path.join(output_dir, filename)
        pdf = creator_fn()
        pdf.output(filepath)
        print(f"  Created: {filepath}")

    print(f"\nDone! {len(resumes)} sample resumes saved to '{output_dir}/'")
    print("You can upload these PDFs in the web app for testing.")


if __name__ == '__main__':
    main()
