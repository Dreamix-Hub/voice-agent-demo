import os
import re

# Define the exact order requested
ORDER = [
    "identity",
    "objectives",
    "personality",
    "conversation_rules",
    "decision_framework",
    "workflows",
    "tool_rules",
    "recovery",
    "voice",
    "safety",
    "closing"
]

OUTPUT_FILE = "system_prompt.md"

def normalize_filename(name):
    """Normalize file name by stripping extension and removing special characters for flexible matching."""
    base = os.path.splitext(name)[0]
    return re.sub(r'[^a-zA-Z0-9]', '', base).lower()

def main():
    # Map current directory files to normalized names
    available_files = {}
    for filename in os.listdir('.'):
        if filename.endswith('.md') and filename != OUTPUT_FILE:
            norm_name = normalize_filename(filename)
            available_files[norm_name] = filename

    merged_content = []
    missing_sections = []

    for section in ORDER:
        norm_section = normalize_filename(section)
        
        if norm_section in available_files:
            file_to_read = available_files[norm_section]
            print(f"[✓] Processing: {section} ({file_to_read})")
            
            with open(file_to_read, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # Append section content with spacing
                merged_content.append(content)
        else:
            missing_sections.append(section)
            print(f"[!] Missing file for section: {section}")

    # Write merged output
    if merged_content:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n\n---\n\n".join(merged_content) + "\n")
        print(f"\nSuccessfully merged {len(merged_content)} section(s) into '{OUTPUT_FILE}'.")
    else:
        print("\nNo matching markdown files were found.")

    if missing_sections:
        print("\nNote: The following sections were not found in the current directory:")
        for miss in missing_sections:
            print(f"  - {miss}")

if __name__ == "__main__":
    main()