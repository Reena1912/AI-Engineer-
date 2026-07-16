import os
import time
import csv  # <-- Added for CSV export
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

job_description = """
Executive - Python
Mumbai, Maharashtra, India
Trending
Job Description
About KPMG in India

KPMG entities in India are professional services firm(s). These Indian member firms are affiliated with KPMG International Limited. KPMG was established in India in August 1993. Our professionals leverage the global network of firms, and are conversant with local laws, regulations, markets and competition. KPMG has offices across India in Ahmedabad, Bengaluru, Chandigarh, Chennai, Gurugram, Jaipur, Hyderabad, Jaipur, Kochi, Kolkata, Mumbai, Noida, Pune, Vadodara and Vijayawada. 

KPMG entities in India offer services to national and international clients in India across sectors. We strive to provide rapid, performance-based, industry-focused and technology-enabled services, which reflect a shared knowledge of global and local industries and our experience of the Indian business environment.

Full stack developer
Equal employment opportunity information 


KPMG India has a policy of providing equal opportunity for all applicants and employees regardless of their color, caste, religion, age, sex/gender, national origin, citizenship, sexual orientation, gender identity or expression, disability or other legally protected status. KPMG India values diversity and we request you to submit the details below to support us in our endeavor for diversity. Providing the below information is voluntary and refusal to submit such information will not be prejudicial to you.
Qualifications
Any Engineering

"""

class JobD(BaseModel):
    role: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: float | None
    education_requirements: list[str]
    responsibilities: list[str]

jobd_schema = JobD.model_json_schema()

system_prompt = f"""
You are an expert HR assistant.

Your job is to analyze job descriptions and extract
structured information from them.

Return ONLY valid JSON matching this schema:

{jobd_schema}
IMPORTANT:
Do NOT return the schema itself.
Do NOT return fields like "properties", "title" or "type".
Fill the schema with actual information extracted from the job description.

If minimum experience is not mentioned, return null.
If information for a list is missing, return an empty list.
Do not invent information.
"""

user_prompt = f"""
Analyze the following job description:

{job_description}
"""
message_system = {
    "role": "system",
    "content": system_prompt
}
message_user = {
    "role": "user",
    "content": user_prompt
}
response_format = {
    "type": "json_object"
}

messages = [message_system, message_user]

response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
answer = response.choices[0].message.content
raw_json = answer

job_data = json.loads(raw_json)
job = JobD(**job_data)

print("Min Experience Required:", job.minimum_experience)
print("Edu Requirements:", job.education_requirements)

# parse real
class MatchResult(BaseModel):
    score: float
    details: dict

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_experience_years: float | None = None
    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []

resume_schema = Resume.model_json_schema()

def final_score(job, resume):
    match_schema = MatchResult.model_json_schema()
    prompt = f"""
    You are an HR recruiter.

    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {resume.model_dump_json(indent=2)}
    Return JSON matching this schema:

    {match_schema}

    Give me:

    1. Candidate name
    2. Matching skills
    3. Missing important skills
    4. Whether experience requirement is met
    5. Overall match percentage from 0 to 100
    6. A short final verdict

    Keep the response concise and easy to read.
    """
    message = {
        "role": "user",
        "content": prompt
    }
    messages = [message]
    response_format = {
        "type": "json_object"
    }
    response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    data = json.loads(response.choices[0].message.content)
    return MatchResult(**data)

def parse_resume(resume_text):
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """
    message_system = {
        "role": "system",
        "content": system_prompt
    }
    message_user = {
        "role": "user",
        "content": user_prompt
    }
    messages = [message_system, message_user]
    response_format = {
        "type": "json_object"
    }
    response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume

from pypdf import PdfReader
from docx import Document

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def read_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"
    return text

def read_resume(file_path):
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        return read_docx(file_path)
    else:
        return None

# lets do it now
resume_folder = Path("resumes")
all_results = []
for file_path in resume_folder.iterdir():
    if file_path.suffix.lower() not in [".pdf", ".docx"]:
        continue
    print("\nProcessing:", file_path.name)
    resume_text = read_resume(file_path)
    parsed_resume = parse_resume(resume_text)  # llm call 1
    time.sleep(5)
    result = final_score(job, parsed_resume)  # llm call 2
    time.sleep(5)
    print("Score:", result.score)
    all_results.append({
        "name": parsed_resume.name or file_path.stem,
        "score": result.score,
        "details": result.details
    })

all_results.sort(
    key=lambda candidate: candidate["score"],
    reverse=True
)

top_2 = all_results[:2]
worst_2 = all_results[-2:]

print("\nTOP 2 CANDIDATES")
for candidate in top_2:
    print(candidate["name"], "-", candidate["score"], "%")
    print(candidate["details"])

print("\nLOWEST 2 CANDIDATES")
for candidate in worst_2:
    print(candidate["name"], "-", candidate["score"], "%")
    print(candidate["details"])

# ==========================================
# NEW: EXPORT RESULT TO CSV
# ==========================================
csv_filename = "evaluation_report.csv"
print(f"\nExporting results to {csv_filename}...")

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write CSV Header
    writer.writerow([
        "Rank", 
        "Candidate Name", 
        "Match Score (%)", 
        "Matching Skills", 
        "Missing Important Skills", 
        "Experience Requirements Met", 
        "Final Verdict"
    ])
    
    # Write data rows
    for index, candidate in enumerate(all_results, 1):
        details = candidate["details"]
        
        # Safely extract details keys in case LLM labels keys slightly differently
        matching_skills = details.get("matching_skills", details.get("2", ""))
        missing_skills = details.get("missing_important_skills", details.get("missing_skills", details.get("3", "")))
        experience_met = details.get("experience_requirement_met", details.get("4", ""))
        verdict = details.get("short_final_verdict", details.get("verdict", details.get("6", "")))
        
        # Convert lists to comma-separated strings if returned as list objects
        if isinstance(matching_skills, list):
            matching_skills = ", ".join(matching_skills)
        if isinstance(missing_skills, list):
            missing_skills = ", ".join(missing_skills)
            
        writer.writerow([
            index,
            candidate["name"],
            f"{candidate['score']}%",
            matching_skills,
            missing_skills,
            experience_met,
            verdict
        ])

print("Export complete!")