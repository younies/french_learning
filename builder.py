#!/usr/bin/env python3
"""
French Learning Repository Link Builder

This script automatically scans the tcf_canada/eo/task2, tcf_canada/eo/task3,
and tcf_canada/ee/task1, tcf_canada/ee/task2, tcf_canada/ee/task3 directories
and generates markdown links for all files, then updates the README.md.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def clean_filename_for_title(filename: str) -> str:
    """
    Convert a filename to a clean, readable title.
    
    Args:
        filename: The original filename
        
    Returns:
        A cleaned title suitable for display
    """
    # Remove .md extension
    title = filename.replace('.md', '')
    
    # Extract task number if present
    task_match = re.match(r'task[123]_(\d+)_(.+)', title)
    if task_match:
        task_num = task_match.group(1)
        content = task_match.group(2)
        
        # Replace underscores with spaces and decode URL-like encoding
        content = content.replace('_', ' ')
        content = content.replace('.', ' ')
        
        # Clean up multiple spaces
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Capitalize first letter
        if content:
            content = content[0].upper() + content[1:]
        
        return f"Numéro {task_num}: {content}"
    
    # Fallback: just clean up the filename
    title = title.replace('_', ' ').replace('.', ' ')
    title = re.sub(r'\s+', ' ', title).strip()
    if title:
        title = title[0].upper() + title[1:]
    
    return title


def scan_directory(dir_path: Path) -> List[Tuple[str, str]]:
    """
    Scan a directory for .md files and return (title, relative_path) pairs.
    
    Args:
        dir_path: Path to the directory to scan
        
    Returns:
        List of (title, relative_path) tuples, sorted by filename
    """
    if not dir_path.exists() or not dir_path.is_dir():
        return []
    
    md_files = []
    for file_path in sorted(dir_path.glob('*.md')):
        title = clean_filename_for_title(file_path.name)
        # Use relative path from the repository root
        relative_path = str(file_path)
        md_files.append((title, relative_path))
    
    return md_files


def generate_markdown_links(files: List[Tuple[str, str]]) -> str:
    """
    Generate markdown link list from file tuples.
    
    Args:
        files: List of (title, path) tuples
        
    Returns:
        Markdown formatted string with bullet points and links
    """
    if not files:
        return "No files found.\n"
    
    links = []
    for title, path in files:
        links.append(f"* [{title}]({path})")
    
    return '\n'.join(links) + '\n'


def update_readme(eo_task2_content: str, eo_task3_content: str, ee_task1_content: str, ee_task2_content: str, ee_task3_content: str) -> None:
    """
    Update the README.md file with new content for all task sections.
    
    Args:
        eo_task2_content: Markdown content for Expression Orale task2 section
        eo_task3_content: Markdown content for Expression Orale task3 section
        ee_task1_content: Markdown content for Expression Écrite task1 section
        ee_task2_content: Markdown content for Expression Écrite task2 section
        ee_task3_content: Markdown content for Expression Écrite task3 section
    """
    readme_path = Path('README.md')
    
    if not readme_path.exists():
        print("README.md not found!")
        return
    
    # Read current README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the TCF Canada section
    tcf_start = "## TCF Canada\n"
    tcf_pos = content.find(tcf_start)
    
    if tcf_pos == -1:
        print("Could not find the TCF Canada section in README.md")
        return
    
    # Extract the part before TCF Canada
    before_tcf = content[:tcf_pos]
    
    # Build the new TCF Canada section with both EE and EO content
    new_tcf_content = f"""## TCF Canada

### Expression Ecrite

#### Tâche 1

{ee_task1_content}

#### Tâche 2

{ee_task2_content}

#### Tâche 3

{ee_task3_content}

### Expression Orale

* [Exam 1](tcf_canada/eo/exam1.md)

#### Tâche 2

{eo_task2_content}

#### Tâche 3

{eo_task3_content}
"""
    
    # Build the complete new content
    new_content = before_tcf + new_tcf_content
    
    # Write the updated content
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("README.md updated successfully!")


def main():
    """Main function to build and update the links."""
    print("French Learning Repository Link Builder")
    print("=" * 40)
    
    # Define paths for Expression Orale
    eo_base_path = Path('tcf_canada/eo')
    eo_task2_path = eo_base_path / 'task2'
    eo_task3_path = eo_base_path / 'task3'
    
    # Define paths for Expression Écrite
    ee_base_path = Path('tcf_canada/ee')
    ee_task1_path = ee_base_path / 'task1'
    ee_task2_path = ee_base_path / 'task2'
    ee_task3_path = ee_base_path / 'task3'
    
    # Scan Expression Orale directories
    print(f"Scanning {eo_task2_path}...")
    eo_task2_files = scan_directory(eo_task2_path)
    print(f"Found {len(eo_task2_files)} files in EO task2")
    
    print(f"Scanning {eo_task3_path}...")
    eo_task3_files = scan_directory(eo_task3_path)
    print(f"Found {len(eo_task3_files)} files in EO task3")
    
    # Scan Expression Écrite directories
    print(f"Scanning {ee_task1_path}...")
    ee_task1_files = scan_directory(ee_task1_path)
    print(f"Found {len(ee_task1_files)} files in EE task1")
    
    print(f"Scanning {ee_task2_path}...")
    ee_task2_files = scan_directory(ee_task2_path)
    print(f"Found {len(ee_task2_files)} files in EE task2")
    
    print(f"Scanning {ee_task3_path}...")
    ee_task3_files = scan_directory(ee_task3_path)
    print(f"Found {len(ee_task3_files)} files in EE task3")
    
    # Generate markdown content
    eo_task2_content = generate_markdown_links(eo_task2_files)
    eo_task3_content = generate_markdown_links(eo_task3_files)
    ee_task1_content = generate_markdown_links(ee_task1_files)
    ee_task2_content = generate_markdown_links(ee_task2_files)
    ee_task3_content = generate_markdown_links(ee_task3_files)
    
    # Preview the content
    print("\nGenerated EO Task 2 content:")
    print("-" * 25)
    print(eo_task2_content)
    
    print("Generated EO Task 3 content:")
    print("-" * 25)
    print(eo_task3_content)
    
    print("Generated EE Task 1 content:")
    print("-" * 25)
    print(ee_task1_content)
    
    print("Generated EE Task 2 content:")
    print("-" * 25)
    print(ee_task2_content)
    
    print("Generated EE Task 3 content:")
    print("-" * 25)
    print(ee_task3_content)
    
    # Update README
    update_readme(eo_task2_content, eo_task3_content, ee_task1_content, ee_task2_content, ee_task3_content)


if __name__ == "__main__":
    main()
