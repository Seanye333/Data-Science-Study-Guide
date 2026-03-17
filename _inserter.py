"""Reusable section inserter with trailing-comma fix."""
import re

def insert_sections(filepath, marker, new_sections_str):
    """Insert new_sections_str before marker, adding comma after last section if needed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    idx = content.rfind(marker)
    if idx == -1:
        # Try bare ] before if __name__
        m = re.search(r'\]\s*\n\s*\nif __name__', content)
        if m:
            idx = m.start()
        else:
            print(f"ERROR: marker not found in {filepath}")
            return False

    # Check if we need a comma before the new sections
    before = content[:idx].rstrip()
    if before.endswith('}') and not before.endswith('},'):
        # Add comma
        content = before + ',\n\n' + new_sections_str + content[idx:]
    else:
        content = content[:idx] + new_sections_str + content[idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK: inserted sections into {filepath}")
    return True
