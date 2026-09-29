#!/usr/bin/env python3
"""
sync_members.py — Automatically scan profile_pics/ and sync with data.js

Usage:
    python3 sync_members.py
"""

import os
import re

PROFILE_DIR = "profile_pics"
DATA_JS = "data.js"

def format_name_from_filename(filename):
    basename = os.path.splitext(filename)[0]
    # Remove leading prefixes like dr_ if present
    if basename.lower().startswith("dr_"):
        parts = basename[3:].split("_")
        name = "Dr. " + " ".join(parts)
    else:
        parts = basename.split("_")
        name = " ".join(parts)
    return name

def make_id(name):
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip().lower()
    return re.sub(r'\s+', '-', clean)

def main():
    if not os.path.exists(PROFILE_DIR) or not os.path.exists(DATA_JS):
        print(f"Error: Missing {PROFILE_DIR} or {DATA_JS}")
        return

    # Valid image extensions
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    pic_files = [f for f in sorted(os.listdir(PROFILE_DIR)) if os.path.splitext(f)[1].lower() in valid_exts]

    with open(DATA_JS, "r", encoding="utf-8") as f:
        content = f.read()

    # Find which images are already in data.js
    missing = []
    for f in pic_files:
        path = f"{PROFILE_DIR}/{f}"
        if path not in content:
            missing.append(f)

    if not missing:
        print("✓ All images in profile_pics/ are already listed in data.js!")
        return

    print(f"Found {len(missing)} new member photo(s): {missing}")

    # Build entry blocks for missing members
    new_entries = []
    for f in missing:
        name = format_name_from_filename(f)
        mid = make_id(name)
        img_path = f"{PROFILE_DIR}/{f}"
        email_prefix = make_id(name).replace("-", "_")
        
        entry = f"""  {{
    id: "{mid}",
    name: "{name}",
    role: "Graduate Researcher",
    category: "MSc",
    image: "{img_path}",
    shortBio: "Researcher focusing on computer vision and machine learning applications.",
    tags: ["Computer Vision", "Deep Learning", "Machine Learning"],
    github: "https://github.com/",
    linkedin: "https://linkedin.com/",
    email: "{email_prefix}@iust.ac.ir",
    location: "Lab Room 404",
    bio: "{name} is a researcher at ICVLab at Iran University of Science and Technology, working on advanced computer vision models.",
    education: ["M.Sc. Student in Computer Engineering, IUST"],
    interests: ["Computer Vision", "Deep Learning", "Artificial Intelligence"],
    publications: [],
    projects: ["Vision AI Models"],
  }},"""
        new_entries.append(entry)

    # Insert before the closing `];` of MEMBERS
    idx = content.rfind("];")
    if idx == -1:
        print("Error: Could not locate '];' in data.js")
        return

    updated_content = content[:idx].rstrip() + "\n" + "\n".join(new_entries) + "\n];\n"

    with open(DATA_JS, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"✓ Successfully added {len(missing)} new member(s) to {DATA_JS}!")

if __name__ == "__main__":
    main()
