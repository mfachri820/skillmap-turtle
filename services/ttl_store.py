import os
import re

TTL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "career_data.ttl",
)


def load_ttl_text():
    with open(TTL_PATH, "r", encoding="utf-8") as handle:
        return handle.read()


def save_ttl_text(content):
    with open(TTL_PATH, "w", encoding="utf-8") as handle:
        handle.write(content)


def parse_skills_from_ttl(content):
    return sorted(set(re.findall(r"^:([A-Za-z0-9_]+)\s+a\s+:Skill", content, re.MULTILINE)))


def parse_roles_from_ttl(content):
    roles = re.findall(r"^:([A-Za-z0-9_]+)\s+rdf:type\s+:CareerRole", content, re.MULTILINE)
    roles += re.findall(r"^:([A-Za-z0-9_]+)\s+a\s+:CareerRole", content, re.MULTILINE)
    return sorted(set(roles))


def append_ttl_block(content, block):
    if not content.endswith("\n"):
        content += "\n"
    return content + "\n" + block.strip() + "\n"


def remove_subject_blocks(content, subjects):
    updated = content
    for subject in subjects:
        pattern = re.compile(rf"^:{re.escape(subject)}\b[\s\S]*?\n\s*\.\s*$", re.MULTILINE)
        updated = re.sub(pattern, "", updated).strip() + "\n"
    return updated


def normalize_id(value):
    return re.sub(r"[^A-Za-z0-9_]", "", value.replace(" ", ""))


def subject_exists(content, subject):
    return re.search(rf"^:{re.escape(subject)}\b", content, re.MULTILINE) is not None
