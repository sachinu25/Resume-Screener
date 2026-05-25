"""
config.py - Centralized configuration for the ATS Screening System
All tunable parameters in one place for easy experimentation
"""

import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'resumes')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
CHART_DIR = os.path.join(STATIC_DIR, 'charts')
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')

# --- Sentence Transformer Model ---
SBERT_MODEL_NAME = 'all-MiniLM-L6-v2'

# --- Scoring Weights (must sum to 1.0) ---
WEIGHT_SEMANTIC = 0.40
WEIGHT_SKILLS = 0.35
WEIGHT_EXPERIENCE = 0.15
WEIGHT_EDUCATION = 0.10

# --- Semantic Score Calibration ---
# Raw cosine similarity from SBERT typically falls in [0.15, 0.70] for resume-JD pairs.
# We map this range to [0, 100] so scores feel realistic.
CALIBRATION_MIN = 0.15   # cosine sim below this → 0%
CALIBRATION_MAX = 0.70   # cosine sim above this → 100%

# --- Skill Synonyms ---
# Maps abbreviations and alternate names to canonical skill names
SKILL_SYNONYMS = {
    'ml': 'machine learning',
    'dl': 'deep learning',
    'ai': 'artificial intelligence',
    'nlp': 'natural language processing',
    'cv': 'computer vision',
    'js': 'javascript',
    'ts': 'typescript',
    'py': 'python',
    'k8s': 'kubernetes',
    'tf': 'tensorflow',
    'sklearn': 'scikit-learn',
    'sci-kit learn': 'scikit-learn',
    'postgres': 'postgresql',
    'mongo': 'mongodb',
    'node': 'node.js',
    'react.js': 'react',
    'reactjs': 'react',
    'angular.js': 'angular',
    'angularjs': 'angular',
    'vue.js': 'vue',
    'vuejs': 'vue',
    'nextjs': 'next.js',
    'express.js': 'express',
    'expressjs': 'express',
    'aws': 'amazon web services',
    'gcp': 'google cloud platform',
    'oop': 'object oriented programming',
    'ci/cd': 'continuous integration',
    'cicd': 'continuous integration',
    'devops': 'devops',
    'swe': 'software engineering',
    'sde': 'software development',
    'dsa': 'data structures and algorithms',
    'rdbms': 'relational database',
    'nosql': 'nosql database',
    'llm': 'large language model',
    'genai': 'generative ai',
    'rag': 'retrieval augmented generation',
    'api': 'application programming interface',
    'rest': 'restful api',
    'graphql': 'graphql',
    'html5': 'html',
    'css3': 'css',
    'sass': 'sass',
    'scss': 'sass',
}

# --- Skill Taxonomy ---
# Organized by category for better extraction and display
SKILL_TAXONOMY = {
    'Programming Languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c',
        'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r',
        'matlab', 'perl', 'lua', 'dart', 'haskell', 'elixir', 'clojure',
        'html', 'css', 'sql', 'bash', 'shell', 'powershell', 'sass',
    ],
    'Web Frameworks': [
        'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring',
        'spring boot', 'node.js', 'express', 'next.js', 'nuxt.js', 'svelte',
        'bootstrap', 'tailwind', 'jquery', '.net', 'asp.net', 'laravel',
        'rails', 'ruby on rails', 'gatsby', 'remix',
    ],
    'Data Science & ML': [
        'machine learning', 'deep learning', 'artificial intelligence',
        'natural language processing', 'computer vision', 'data science',
        'data analysis', 'data engineering', 'data mining', 'big data',
        'statistics', 'data visualization', 'feature engineering',
        'neural networks', 'reinforcement learning', 'transfer learning',
        'generative ai', 'large language model', 'prompt engineering',
        'retrieval augmented generation', 'mlops',
    ],
    'ML Libraries': [
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
        'matplotlib', 'seaborn', 'plotly', 'scipy', 'xgboost', 'lightgbm',
        'catboost', 'opencv', 'spacy', 'nltk', 'hugging face', 'transformers',
        'langchain', 'llamaindex', 'openai api',
    ],
    'Databases': [
        'mysql', 'postgresql', 'mongodb', 'sqlite', 'redis', 'oracle',
        'cassandra', 'dynamodb', 'firebase', 'elasticsearch', 'neo4j',
        'mariadb', 'couchdb', 'influxdb', 'supabase', 'cockroachdb',
        'sql server', 'snowflake', 'bigquery', 'redshift',
    ],
    'Cloud & DevOps': [
        'aws', 'amazon web services', 'azure', 'google cloud platform',
        'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
        'continuous integration', 'github actions', 'gitlab ci',
        'circleci', 'vagrant', 'puppet', 'chef', 'helm',
        'cloudformation', 'pulumi',
    ],
    'Tools & Platforms': [
        'git', 'github', 'gitlab', 'bitbucket', 'linux', 'nginx',
        'apache', 'jira', 'confluence', 'slack', 'figma', 'photoshop',
        'vs code', 'intellij', 'jupyter', 'google colab', 'postman',
        'swagger', 'grafana', 'prometheus', 'datadog', 'splunk',
        'tableau', 'power bi', 'excel', 'looker',
    ],
    'Architecture & Concepts': [
        'microservices', 'restful api', 'graphql', 'api', 'grpc',
        'message queue', 'kafka', 'rabbitmq', 'event driven',
        'serverless', 'lambda', 'cloud functions',
        'agile', 'scrum', 'kanban', 'tdd', 'bdd',
        'object oriented programming', 'functional programming',
        'design patterns', 'solid principles', 'clean architecture',
        'system design', 'distributed systems', 'load balancing',
        'caching', 'cdn', 'oauth', 'jwt', 'websockets',
    ],
    'Testing': [
        'unit testing', 'integration testing', 'testing', 'automation',
        'selenium', 'cypress', 'jest', 'pytest', 'junit', 'mocha',
        'playwright', 'test driven development',
    ],
    'Mobile': [
        'android', 'ios', 'react native', 'flutter', 'xamarin',
        'swift ui', 'jetpack compose', 'mobile development',
    ],
    'Soft Skills': [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'project management', 'analytical', 'critical thinking',
        'presentation', 'mentoring', 'collaboration', 'time management',
    ],
    'Security': [
        'cybersecurity', 'information security', 'penetration testing',
        'encryption', 'firewall', 'siem', 'soc', 'ethical hacking',
        'vulnerability assessment', 'owasp',
    ],
    'Data Engineering': [
        'hadoop', 'spark', 'apache spark', 'hive', 'airflow',
        'etl', 'data pipeline', 'data warehouse', 'data lake',
        'dbt', 'presto', 'flink', 'beam', 'nifi',
    ],
}

# Flatten taxonomy into a single list for quick lookup
ALL_SKILLS = []
for category_skills in SKILL_TAXONOMY.values():
    ALL_SKILLS.extend(category_skills)
ALL_SKILLS = list(set(ALL_SKILLS))  # deduplicate

# --- Education Levels (ordered by rank) ---
EDUCATION_LEVELS = {
    'phd': 5,
    'ph.d': 5,
    'doctorate': 5,
    'doctoral': 5,
    'master': 4,
    'masters': 4,
    'm.s.': 4,
    'm.sc': 4,
    'msc': 4,
    'mba': 4,
    'm.tech': 4,
    'mtech': 4,
    'm.e.': 4,
    'bachelor': 3,
    'bachelors': 3,
    'b.s.': 3,
    'b.sc': 3,
    'bsc': 3,
    'b.tech': 3,
    'btech': 3,
    'b.e.': 3,
    'b.a.': 3,
    'associate': 2,
    'diploma': 2,
    'certification': 1,
    'certificate': 1,
    'bootcamp': 1,
}

# --- Section Headers for Resume Parsing ---
SECTION_HEADERS = {
    'experience': ['experience', 'work experience', 'professional experience',
                    'employment', 'work history', 'career history'],
    'education': ['education', 'academic', 'qualification', 'qualifications',
                  'academic background', 'educational background'],
    'skills': ['skills', 'technical skills', 'core competencies', 'competencies',
               'technologies', 'tech stack', 'tools', 'proficiencies'],
    'projects': ['projects', 'personal projects', 'academic projects',
                 'key projects', 'side projects'],
    'summary': ['summary', 'objective', 'about me', 'profile', 'about',
                'professional summary', 'career objective', 'career summary'],
    'certifications': ['certifications', 'certificates', 'licenses',
                       'professional development', 'training'],
    'publications': ['publications', 'papers', 'research'],
}

# --- Flask Config ---
FLASK_SECRET_KEY = 'ats-screener-2024-secure-key'
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB total
MAX_FILE_SIZE = 10 * 1024 * 1024    # 10 MB per file
