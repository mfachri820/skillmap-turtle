from SPARQLWrapper import SPARQLWrapper, JSON

# Sesuaikan URL ini dengan endpoint Fuseki kalian nanti
FUSEKI_ENDPOINT = "http://localhost:3030/skillmap-ai/query"

def get_role_by_skill(skill_name):
    """
    Fungsi dasar untuk mencari role berdasarkan nama skill.
    """
    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
    
    # Query dasar: Mencari role yang memiliki skill tertentu
    query = f"""
    PREFIX : <http://example.org/skillmap#>
    SELECT ?roleName
    WHERE {{
      ?role a :CareerRole ;
            :roleName ?roleName ;
            :requiresSkill ?skillURI .
      ?skillURI :skillName ?name .
      FILTER(CONTAINS(LCASE(?name), LCASE("{skill_name}")))
    }}
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        roles = []
        for result in results["results"]["bindings"]:
            roles.append(result["roleName"]["value"])
        return roles
    except Exception as e:
        raise ConnectionError(f"Error koneksi ke Fuseki: {e}")


def get_roles_by_skills(skills):
    """Search career roles for a list of skills using Fuseki."""
    results = []
    for skill in skills:
        roles = get_role_by_skill(skill)
        for role in roles:
            if role not in results:
                results.append(role)
    return results


def get_jobs_by_skills(skills, use_and=False):
    """
    Search job postings by skills.
    If use_and=True: job must have ALL skills (AND logic)
    If use_and=False: job can have ANY skill (OR logic)
    """
    if not skills:
        return []

    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
    
    if use_and and len(skills) > 1:
        # AND logic: fetch all jobs with any of the skills, then filter in Python
        filters = " || ".join(
            f'CONTAINS(LCASE(?skillName), LCASE("{skill}"))'
            for skill in skills
        )
        
        query = f"""
        PREFIX : <http://example.org/skillmap#>
        SELECT DISTINCT ?jobTitle ?companyName ?jobDescription ?vacancyCount (GROUP_CONCAT(DISTINCT ?skillName; separator="|") AS ?skills)
        WHERE {{
          ?job a :JobPosting ;
               :jobTitle ?jobTitle ;
               :requiredSkill ?skillURI ;
               :jobDescription ?jobDescription ;
               :vacancyCount ?vacancyCount .
          OPTIONAL {{
            ?job :employer ?employer .
            ?employer :companyName ?companyName .
          }}
          ?skillURI :skillName ?skillName .
          FILTER({filters})
        }}
        GROUP BY ?jobTitle ?companyName ?jobDescription ?vacancyCount
        ORDER BY LCASE(?jobTitle)
        """
    else:
        # OR logic: job can have any of the skills
        filters = " || ".join(
            f'CONTAINS(LCASE(?skillName), LCASE("{skill}"))'
            for skill in skills
        )
        
        query = f"""
        PREFIX : <http://example.org/skillmap#>
        SELECT DISTINCT ?jobTitle ?companyName ?jobDescription ?vacancyCount (GROUP_CONCAT(DISTINCT ?skillName; separator="|") AS ?skills)
        WHERE {{
          ?job a :JobPosting ;
               :jobTitle ?jobTitle ;
               :requiredSkill ?skillURI ;
               :jobDescription ?jobDescription ;
               :vacancyCount ?vacancyCount .
          OPTIONAL {{
            ?job :employer ?employer .
            ?employer :companyName ?companyName .
          }}
          ?skillURI :skillName ?skillName .
          FILTER({filters})
        }}
        GROUP BY ?jobTitle ?companyName ?jobDescription ?vacancyCount
        ORDER BY LCASE(?jobTitle)
        """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        jobs = []
        for result in results["results"]["bindings"]:
            skills_raw = result["skills"]["value"]
            job_skills = [skill for skill in skills_raw.split("|") if skill]
            company = result.get("companyName", {}).get("value", "Perusahaan Terdaftar")
            description = result.get("jobDescription", {}).get("value", "Tidak ada deskripsi tersedia.")
            vacancy = result.get("vacancyCount", {}).get("value", "0")
            
            # Only apply AND filtering if use_and is True and we have multiple skills
            if use_and and len(skills) > 1:
                search_skills_lower = [s.lower() for s in skills]
                job_skills_lower = [s.lower() for s in job_skills]
                
                # Check if ALL searched skills are in this job's skills
                if all(any(search_skill in job_skill for job_skill in job_skills_lower) for search_skill in search_skills_lower):
                    jobs.append({
                        "jobTitle": result["jobTitle"]["value"],
                        "company": company,
                        "description": description,
                        "vacancy": vacancy,
                        "skills": job_skills,
                    })
            else:
                # OR logic: include all jobs returned by the query
                jobs.append({
                    "jobTitle": result["jobTitle"]["value"],
                    "company": company,
                    "description": description,
                    "vacancy": vacancy,
                    "skills": job_skills,
                })
        return jobs
    except Exception as e:
        raise ConnectionError(f"Error koneksi ke Fuseki: {e}")


def get_all_roles_with_skills():
    """Return all job postings with their required skills and employer names."""
    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)

    query = """
    PREFIX : <http://example.org/skillmap#>
    SELECT ?jobTitle ?companyName ?jobDescription ?vacancyCount (GROUP_CONCAT(DISTINCT ?skillName; separator="|") AS ?skills)
    WHERE {
      ?job a :JobPosting ;
           :jobTitle ?jobTitle ;
           :requiredSkill ?skillURI ;
           :jobDescription ?jobDescription ;
           :vacancyCount ?vacancyCount .
      OPTIONAL {
        ?job :employer ?employer .
        ?employer :companyName ?companyName .
      }
      ?skillURI :skillName ?skillName .
    }
    GROUP BY ?jobTitle ?companyName ?jobDescription ?vacancyCount
    ORDER BY LCASE(?jobTitle)
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        roles = []
        for result in results["results"]["bindings"]:
            skills_raw = result["skills"]["value"]
            skills = [skill for skill in skills_raw.split("|") if skill]
            company = result.get("companyName", {}).get("value", "Perusahaan Terdaftar")
            description = result.get("jobDescription", {}).get("value", "Tidak ada deskripsi tersedia.")
            vacancy = result.get("vacancyCount", {}).get("value", "0")
            roles.append({
                "role": result["jobTitle"]["value"],
                "company": company,
                "description": description,
                "vacancy": vacancy,
                "skills": skills,
            })
        return roles
    except Exception as e:
        raise ConnectionError(f"Error koneksi ke Fuseki: {e}")

