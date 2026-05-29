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


def get_jobs_by_skills(skills):
    """Search job postings that require one or more of the given skills."""
    if not skills:
        return []

    filters = " || ".join(
        f'CONTAINS(LCASE(?skillName), LCASE("{skill}"))'
        for skill in skills
    )

    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
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
            skills = [skill for skill in skills_raw.split("|") if skill]
            company = result.get("companyName", {}).get("value", "Perusahaan Terdaftar")
            description = result.get("jobDescription", {}).get("value", "Tidak ada deskripsi tersedia.")
            vacancy = result.get("vacancyCount", {}).get("value", "0")
            jobs.append({
                "jobTitle": result["jobTitle"]["value"],
                "company": company,
                "description": description,
                "vacancy": vacancy,
                "skills": skills,
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

