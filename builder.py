#!/usr/bin/env python3
"""
French Learning Repository Link Builder

This script automatically scans the tcf_canada/eo/task2 and tcf_canada/eo/task3 
directories and generates markdown links for all files, then updates the README.md.
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
    task_match = re.match(r'task[23]_(\d+)_(.+)', title)
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


def update_readme(task2_content: str, task3_content: str) -> None:
    """
    Update the README.md file with new content for task2 and task3 sections.
    
    Args:
        task2_content: Markdown content for task2 section
        task3_content: Markdown content for task3 section
    """
    readme_path = Path('README.md')
    
    if not readme_path.exists():
        print("README.md not found!")
        return
    
    # Read current README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the sections to replace
    task2_start = "## New Expression Orale Tâche 2\n"
    task3_start = "## New Expression Orale Tâche 3\n"
    
    # Find the positions of each section
    task2_pos = content.find(task2_start)
    task3_pos = content.find(task3_start)
    
    if task2_pos == -1 or task3_pos == -1:
        print("Could not find the required sections in README.md")
        return
    
    # Extract the parts of the README
    before_task2 = content[:task2_pos]
    
    # Find the end of task2 section (start of task3 section)
    task2_end = task3_pos
    
    # Find the end of task3 section (end of file or next major section)
    after_task3_pos = len(content)  # Default to end of file
    
    # Build the new content
    new_content = (
        before_task2 +
        task2_start + "\n" + task2_content + "\n\n" +
        task3_start + "\n" + task3_content
    )
    
    # Write the updated content
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("README.md updated successfully!")


def main():
    """Main function to build and update the links."""
    print("French Learning Repository Link Builder")
    print("=" * 40)
    
    # Define paths
    base_path = Path('tcf_canada/eo')
    task2_path = base_path / 'task2'
    task3_path = base_path / 'task3'
    
    # Scan directories
    print(f"Scanning {task2_path}...")
    task2_files = scan_directory(task2_path)
    print(f"Found {len(task2_files)} files in task2")
    
    print(f"Scanning {task3_path}...")
    task3_files = scan_directory(task3_path)
    print(f"Found {len(task3_files)} files in task3")
    
    # Generate markdown content
    task2_content = generate_markdown_links(task2_files)
    task3_content = generate_markdown_links(task3_files)
    
    # Preview the content
    print("\nGenerated Task 2 content:")
    print("-" * 25)
    print(task2_content)
    
    print("Generated Task 3 content:")
    print("-" * 25)
    print(task3_content)
    
    # Update README
    update_readme(task2_content, task3_content)


if __name__ == "__main__":
    main()
