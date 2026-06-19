# SkillMap AI - Project Documentation for Academic Paper

## Project Overview

**SkillMap AI** is a semantic web-based career exploration system that combines:
- **RDF (Resource Description Framework)** knowledge graph for representing skills and job postings
- **Apache Jena Fuseki** as a SPARQL endpoint for querying the knowledge graph
- **Streamlit** web application with an AI-powered conversational interface
- **OpenRouter AI** for natural language processing and skill extraction

The system helps users explore career paths by matching their skills and interests with job postings stored in a semantic graph database.

---

## 1. Dataset Description

### 1.1 Ontology Structure

The dataset uses **RDF/Turtle (TTL)** format with a custom ontology defined at `http://example.org/skillmap#`.

**Core Classes:**
- `:Skill` - Individual skills (e.g., Python, SQL, Figma)
- `:CareerRole` - Job roles (e.g., Data Analyst, UI/UX Designer)
- `:JobPosting` - Actual job listings with details
- `:Employer` - Companies offering jobs
- `:Location` - Job locations
- `:Applicant`, `:Resume`, `:Application` - For future expansion

**Key Properties:**
- `:requiresSkill` - Links roles/jobs to required skills
- `:skillName` - Human-readable skill name
- `:roleName` - Role title
- `:jobTitle`, `:jobDescription`, `:vacancyCount` - Job details
- `:companyName`, `:industry` - Employer information
- `:city`, `:country` - Location data

### 1.2 Dataset Statistics

**Skills:** 40+ skills including:
- **Technical:** Python, SQL, JavaScript, React, Node.js, Machine Learning, DevOps
- **Design:** Figma, User Research, Wireframing, Product Design
- **Business:** Project Management, Communication, Teamwork, Leadership
- **Data:** Excel, Data Visualization, Tableau, Power BI

**Job Postings:** 6+ job listings with:
- Required and preferred skills
- Employment type (Full-Time, Contract, Remote)
- Salary ranges in IDR
- Application deadlines

**Career Roles:** 5 predefined roles:
- Data Analyst
- UI/UX Designer
- Full Stack Developer
- Product Manager
- Business Analyst

### 1.3 Sample Data Structure

```turtle
:Python a :Skill ; :skillName "Python Programming" .

:DataAnalyst rdf:type :CareerRole ;
    :roleName "Data Analyst" ;
    :requiresSkill :Python, :SQL, :Excel, :DataVisualization, :Communication .

:Job_1234 a :JobPosting ;
    :jobTitle "Junior Data Analyst" ;
    :employer :Company_SkylineTech ;
    :requiredSkill :Python, :SQL, :Excel ;
    :vacancyCount 2 ;
    :salaryRange "Rp 7,000,000 - Rp 10,000,000" .
```

---

## 2. Methodology

### 2.1 Semantic Web Approach

The project follows **semantic web principles**:
1. **Knowledge Representation:** Skills, jobs, and relationships are modeled as RDF triples
2. **Ontology Design:** Custom vocabulary defines classes and properties for career domain
3. **Graph Database:** Apache Jena TDB2 stores RDF data as a knowledge graph
4. **SPARQL Queries:** Semantic queries retrieve data based on relationships, not just keywords

### 2.2 Query Processing Pipeline

**Step 1: User Input Processing**
- User enters skills via multiselect dropdown OR free-text input
- AI decoder (OpenRouter) extracts standardized skill names from natural language
- Example: "I love making dashboards" → "Data Visualization", "Excel"

**Step 2: SPARQL Query Construction**
- Dynamic SPARQL queries built based on selected skills
- Two matching modes:
  - **OR Logic (Toleran):** Match jobs with ANY selected skill
  - **AND Logic (Ketat):** Match jobs with ALL selected skills

**Step 3: Query Execution**
- Queries sent to Fuseki SPARQL endpoint (`http://localhost:3030/skillmap-ai/query`)
- Results returned in JSON format
- Python backend processes and filters results

**Step 4: Result Presentation**
- Streamlit renders job cards with:
  - Job title, company, description
  - Required skills as tags
  - Vacancy count
  - Match explanation

### 2.3 AND/OR Logic Implementation

**OR Logic (Toleran):**
```sparql
FILTER(CONTAINS(LCASE(?skillName), LCASE("Python")) || 
       CONTAINS(LCASE(?skillName), LCASE("SQL")))
```
Returns jobs requiring Python OR SQL (broader results).

**AND Logic (Ketat):**
```python
# Python post-filtering after initial OR query
if all(any(search_skill in job_skill for job_skill in job_skills) 
       for search_skill in search_skills):
    # Include job only if ALL skills match
```
Returns jobs requiring Python AND SQL (more specific results).

### 2.4 AI Integration

**Purpose:** Bridge natural language and structured skills
- **Input:** Free-text user description (e.g., "I like building apps")
- **Processing:** OpenRouter API with GPT model
- **Output:** Standardized skill names from `SKILL_KEYWORD_MAP`
- **Fallback:** If AI unavailable, use keyword matching

---

## 3. System Architecture

### 3.1 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.10+ | Core logic and SPARQL queries |
| **Frontend** | Streamlit | Interactive web UI |
| **Database** | Apache Jena Fuseki | RDF triple store with SPARQL endpoint |
| **AI Service** | OpenRouter API | Natural language to skill mapping |
| **Data Format** | RDF/Turtle | Semantic knowledge representation |
| **Query Language** | SPARQL | Semantic graph queries |

### 3.2 Directory Structure

```
skillmap-ai-semweb/
├── app.py                    # Streamlit entry point
├── config.py                # Theme and skill configurations
├── sparql_client.py        # Fuseki connection and queries
├── data/
│   ├── career_data.ttl     # Main RDF dataset
│   └── bulk_jobs_update.ru # SPARQL UPDATE queries
├── services/
│   ├── ai_client.py        # OpenRouter AI integration
│   ├── auth.py             # Authentication (future)
│   └── session_state.py    # Streamlit state management
├── ui/
│   ├── user_view.py        # Search and results UI
│   ├── admin_view.py       # Admin panel for data management
│   └── styles.py          # CSS styling
└── requirements.txt         # Python dependencies
```

### 3.3 Data Flow Diagram

```
[User Input] 
    ↓
[Streamlit UI] → [AI Decoder (optional)] → [Skill Extraction]
    ↓
[SPARQL Query Builder] → [Fuseki Endpoint] → [RDF Dataset]
    ↓
[JSON Results] → [Python Processing] → [Streamlit Display]
```

---

## 4. Key Features

### 4.1 Search Tab ("Peta Karier, Versi Kamu")
- **Multiselect dropdown:** Choose from 40+ predefined skills
- **Free-text input:** Describe skills/interests in natural language
- **AI decoding:** Converts natural language to standardized skills
- **OR/AND toggle:** Choose matching strictness
- **Results display:** Job cards with skills, company, vacancy

### 4.2 View Jobs Tab ("Jelajahi Career Role")
- **Browse all jobs:** Complete job listing from dataset
- **Skill filtering:** Filter by one or multiple skills
- **OR/AND toggle:** Control filter strictness
- **Search by role:** Text search for job titles

### 4.3 AI Assistant Tab
- **Conversational interface:** Chat about career interests
- **Personalized recommendations:** Based on discussion history
- **Skill discovery:** AI suggests relevant skills

### 4.4 Admin Panel
- **Add new jobs:** Form to insert job postings via SPARQL UPDATE
- **Add new roles:** Create career roles with required skills
- **Bulk operations:** Upload multiple jobs at once

---

## 5. SPARQL Query Examples

### 5.1 Find Jobs by Skill (OR Logic)

```sparql
PREFIX : <http://example.org/skillmap#>
SELECT DISTINCT ?jobTitle ?companyName ?vacancyCount 
       (GROUP_CONCAT(?skillName; separator="|") AS ?skills)
WHERE {
  ?job a :JobPosting ;
       :jobTitle ?jobTitle ;
       :requiredSkill ?skillURI ;
       :vacancyCount ?vacancyCount .
  OPTIONAL {
    ?job :employer ?employer .
    ?employer :companyName ?companyName .
  }
  ?skillURI :skillName ?skillName .
  FILTER(CONTAINS(LCASE(?skillName), LCASE("Python")) || 
         CONTAINS(LCASE(?skillName), LCASE("SQL")))
}
GROUP BY ?jobTitle ?companyName ?vacancyCount
```

### 5.2 Find Jobs Requiring ALL Skills (AND Logic)

Uses post-query Python filtering:
```python
# After fetching candidates with OR query
if all(any(search_skill in job_skill for job_skill in job_skills) 
       for search_skill in ["Python", "SQL"]):
    # Include job
```

### 5.3 Add New Job Posting

```sparql
PREFIX : <http://example.org/skillmap#>
INSERT DATA {
  :Job_9999 a :JobPosting ;
             :jobTitle "Data Engineer" ;
             :employer :Company_SkylineTech ;
             :requiredSkill :Python, :SQL, :DataEngineering ;
             :vacancyCount 2 ;
             :jobDescription "Build data pipelines..." .
}
```

---

## 6. Research Contributions

### 6.1 Academic Value

1. **Semantic Web Application:** Practical implementation of RDF/SPARQL in career matching
2. **Hybrid Query Logic:** Combines SPARQL OR queries with Python AND filtering
3. **Natural Language Interface:** AI bridges unstructured input and structured queries
4. **User-Centric Design:** Toggle between strict (AND) and flexible (OR) matching

### 6.2 Innovation Points

- **Dynamic OR/AND toggle:** User-controlled query strictness
- **AI-enhanced skill extraction:** From free text to standardized ontology terms
- **Conversational career exploration:** AI Assistant for personalized guidance
- **Admin self-service:** Non-technical users can update the knowledge graph

---

## 7. Future Enhancements

1. **Inference Rules:** Use OWL reasoning to infer related skills
2. **Skill Similarity:** Semantic similarity beyond exact string matching
3. **User Profiles:** Save career preferences and history
4. **Recommendation Engine:** Suggest skills to learn for target roles
5. **Multi-language Support:** Indonesian ↔ English skill mapping

---

## 8. How to Run the Project

### 8.1 Prerequisites
- Python 3.10+
- Apache Jena Fuseki 6.1.0+
- OpenRouter API key

### 8.2 Setup Steps

```bash
# 1. Start Fuseki
cd apache-jena-fuseki-6.1.0
.\fuseki-server.bat

# 2. Load dataset (via Fuseki UI at http://localhost:3030)
# Upload data/career_data.ttl to "skillmap-ai" dataset

# 3. Install Python dependencies
cd skillmap-ai-semweb
pip install -r requirements.txt

# 4. Set OpenRouter API key
echo OPENROUTER_API_KEY=your_key_here > .env

# 5. Run Streamlit
streamlit run app.py
```

### 8.3 Access Points
- **Streamlit App:** http://localhost:8501
- **Fuseki Admin:** http://localhost:3030
- **SPARQL Endpoint:** http://localhost:3030/skillmap-ai/query

---

## 9. Paper Writing Guidelines for Gemini

When writing the academic paper, please emphasize:

1. **Problem Statement:** Career exploration is fragmented; semantic web can unify skills and jobs
2. **Methodology:** How RDF modeling + SPARQL + AI creates intelligent matching
3. **Implementation:** Technical details of OR/AND logic, AI integration
4. **Evaluation:** Discuss trade-offs between OR (recall) and AND (precision)
5. **Contributions:** Practical semantic web application with user-centric design
6. **Future Work:** Scaling to larger datasets, adding inference, multi-language support

**Suggested Paper Structure:**
1. Introduction
2. Literature Review (Semantic Web, Career Matching Systems)
3. System Design & Methodology
4. Implementation Details
5. Evaluation & Discussion
6. Conclusion & Future Work

---

## 10. Contact & Repository

- **Project Location:** `E:\CodeToolsD\Semester 6\Semantik Web\skillmap-ai-semweb\`
- **Dataset:** `data/career_data.ttl`
- **Documentation:** This file (`paperhandover.md`)

---

**End of Documentation**

*This document provides comprehensive context for writing an academic paper about SkillMap AI. Use this to explain the dataset structure, methodology, system design, and research contributions.*
