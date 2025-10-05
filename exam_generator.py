#!/usr/bin/env python3
"""
TCF Complete Exams Generator

This script creates a tcf_complete_exams folder with complete exam files.
Each exam file contains links to Expression Orale (EO) and Expression Écrite (EE) tasks.
Tasks are selected sequentially (exam1 uses task_001, exam2 uses task_002, etc.).
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple


def get_all_task_files(base_path: Path) -> Dict[str, List[str]]:
    """
    Get all task files organized by task type.
    
    Returns:
        Dictionary with task types as keys and lists of file paths as values
    """
    task_files = {
        'eo_task2': [],
        'eo_task3': [],
        'ee_task1': [],
        'ee_task2': [],
        'ee_task3': []
    }
    
    # Expression Orale files
    eo_task2_path = base_path / 'tcf_canada' / 'eo' / 'task2'
    eo_task3_path = base_path / 'tcf_canada' / 'eo' / 'task3'
    
    # Expression Écrite files
    ee_task1_path = base_path / 'tcf_canada' / 'ee' / 'task1'
    ee_task2_path = base_path / 'tcf_canada' / 'ee' / 'task2'
    ee_task3_path = base_path / 'tcf_canada' / 'ee' / 'task3'
    
    # Collect all .md files
    if eo_task2_path.exists():
        task_files['eo_task2'] = sorted([str(f) for f in eo_task2_path.glob('*.md')])
    
    if eo_task3_path.exists():
        task_files['eo_task3'] = sorted([str(f) for f in eo_task3_path.glob('*.md')])
    
    if ee_task1_path.exists():
        task_files['ee_task1'] = sorted([str(f) for f in ee_task1_path.glob('*.md')])
    
    if ee_task2_path.exists():
        task_files['ee_task2'] = sorted([str(f) for f in ee_task2_path.glob('*.md')])
    
    if ee_task3_path.exists():
        task_files['ee_task3'] = sorted([str(f) for f in ee_task3_path.glob('*.md')])
    
    return task_files


def clean_filename_for_title(filename: str) -> str:
    """
    Convert a filename to a clean, readable title.
    """
    # Get just the filename without path
    filename = Path(filename).name
    
    # Remove .md extension
    title = filename.replace('.md', '')
    
    # Replace underscores with spaces
    title = title.replace('_', ' ')
    
    # Clean up multiple spaces
    title = ' '.join(title.split())
    
    # Capitalize first letter
    if title:
        title = title[0].upper() + title[1:]
    
    return title


def generate_exam_content(exam_number: int, task_files: Dict[str, List[str]], base_path: Path) -> str:
    """
    Generate content for a complete exam file.
    
    Args:
        exam_number: The exam number
        task_files: Dictionary of all available task files
        base_path: Base path for relative links
        
    Returns:
        Markdown content for the exam
    """
    
    # Select files sequentially based on exam number (exam_number - 1 for 0-based indexing)
    selected_files = {}
    for task_type, files in task_files.items():
        if files:
            # Use modulo to cycle through available files if we have more exams than files
            file_index = (exam_number - 1) % len(files)
            selected_files[task_type] = files[file_index]
    
    # Generate the exam content
    content = f"""# TCF Canada - Examen Complet {exam_number}

Ce fichier contient un examen complet du TCF Canada avec toutes les tâches d'Expression Orale et d'Expression Écrite.

## 📋 Structure de l'examen

### Expression Orale (EO)
- **Tâche 2** : Conversation simulée
- **Tâche 3** : Monologue suivi

### Expression Écrite (EE)  
- **Tâche 1** : Message personnel (60-120 mots)
- **Tâche 2** : Article de blog (120-150 mots)
- **Tâche 3** : Essai argumentatif (120-180 mots)

---

## 🗣️ Expression Orale

### Tâche 2 - Conversation simulée
"""

    # Add EO Task 2 link
    if 'eo_task2' in selected_files:
        relative_path = os.path.relpath(selected_files['eo_task2'], base_path)
        title = clean_filename_for_title(selected_files['eo_task2'])
        content += f"\n**📄 Sujet sélectionné :** [{title}]({relative_path})\n"
    else:
        content += "\n*Aucun sujet disponible pour cette tâche.*\n"

    content += """
### Tâche 3 - Monologue suivi
"""

    # Add EO Task 3 link
    if 'eo_task3' in selected_files:
        relative_path = os.path.relpath(selected_files['eo_task3'], base_path)
        title = clean_filename_for_title(selected_files['eo_task3'])
        content += f"\n**📄 Sujet sélectionné :** [{title}]({relative_path})\n"
    else:
        content += "\n*Aucun sujet disponible pour cette tâche.*\n"

    content += """
---

## ✍️ Expression Écrite

### Tâche 1 - Message personnel (60-120 mots)
"""

    # Add EE Task 1 link
    if 'ee_task1' in selected_files:
        relative_path = os.path.relpath(selected_files['ee_task1'], base_path)
        title = clean_filename_for_title(selected_files['ee_task1'])
        content += f"\n**📄 Sujet sélectionné :** [{title}]({relative_path})\n"
    else:
        content += "\n*Aucun sujet disponible pour cette tâche.*\n"

    content += """
### Tâche 2 - Article de blog (120-150 mots)
"""

    # Add EE Task 2 link
    if 'ee_task2' in selected_files:
        relative_path = os.path.relpath(selected_files['ee_task2'], base_path)
        title = clean_filename_for_title(selected_files['ee_task2'])
        content += f"\n**📄 Sujet sélectionné :** [{title}]({relative_path})\n"
    else:
        content += "\n*Aucun sujet disponible pour cette tâche.*\n"

    content += """
### Tâche 3 - Essai argumentatif (120-180 mots)
"""

    # Add EE Task 3 link
    if 'ee_task3' in selected_files:
        relative_path = os.path.relpath(selected_files['ee_task3'], base_path)
        title = clean_filename_for_title(selected_files['ee_task3'])
        content += f"\n**📄 Sujet sélectionné :** [{title}]({relative_path})\n"
    else:
        content += "\n*Aucun sujet disponible pour cette tâche.*\n"

    content += """
---

## 📝 Instructions

1. **Temps recommandé :**
   - Expression Orale : 12 minutes au total
     - Tâche 2 : 5-7 minutes
     - Tâche 3 : 4-5 minutes
   - Expression Écrite : 60 minutes au total
     - Tâche 1 : 15 minutes
     - Tâche 2 : 20 minutes  
     - Tâche 3 : 25 minutes

2. **Conseils :**
   - Lisez attentivement chaque sujet avant de commencer
   - Respectez les limites de mots indiquées
   - Structurez vos réponses de manière claire
   - Utilisez un vocabulaire varié et approprié

3. **Évaluation :**
   - Adéquation du discours à la situation de communication
   - Capacité à présenter et défendre un point de vue
   - Cohérence et cohésion du discours
   - Lexique et morphosyntaxe

---

*Bonne chance pour votre examen ! 🍀*
"""

    return content


def create_complete_exams(base_path: Path, num_exams: int = 10) -> None:
    """
    Create complete exam files in the tcf_complete_exams folder.
    
    Args:
        base_path: Base path of the project
        num_exams: Number of exams to generate
    """
    
    print(f"TCF Complete Exams Generator")
    print("=" * 40)
    
    # Create the output directory
    output_dir = base_path / 'tcf_complete_exams'
    output_dir.mkdir(exist_ok=True)
    print(f"Created directory: {output_dir}")
    
    # Get all task files
    print("Scanning task files...")
    task_files = get_all_task_files(base_path)
    
    # Print statistics
    for task_type, files in task_files.items():
        print(f"  {task_type}: {len(files)} files")
    
    # Generate exam files
    print(f"\nGenerating {num_exams} complete exams...")
    
    for i in range(1, num_exams + 1):
        exam_content = generate_exam_content(i, task_files, base_path)
        exam_file = output_dir / f'exam{i:02d}.md'
        
        with open(exam_file, 'w', encoding='utf-8') as f:
            f.write(exam_content)
        
        print(f"  ✓ Created {exam_file.name}")
    
    print(f"\n🎉 Successfully generated {num_exams} complete exams!")
    print(f"📁 Files are located in: {output_dir}")
    
    # Create an index file
    create_index_file(output_dir, num_exams)
    
    # Update main README
    update_main_readme(base_path, num_exams)


def create_index_file(output_dir: Path, num_exams: int) -> None:
    """
    Create an index file listing all generated exams.
    """
    
    index_content = """# TCF Canada - Examens Complets

🏠 **[← Retour au README principal](../README.md)**

Ce dossier contient des examens complets du TCF Canada, chacun incluant toutes les tâches d'Expression Orale et d'Expression Écrite avec sélection séquentielle des sujets.

## 🎯 Accès rapide

| Examen | Lien direct | Description |
|--------|-------------|-------------|"""
    
    for i in range(1, num_exams + 1):
        index_content += f"\n| **Examen {i:02d}** | [📄 exam{i:02d}.md](exam{i:02d}.md) | EO: task_{i:03d} + EE: task_{i:03d} |"
    
    index_content += f"""

## 📚 Liste détaillée des examens

"""
    
    for i in range(1, num_exams + 1):
        index_content += f"### [Examen {i:02d}](exam{i:02d}.md)\n"
        index_content += f"- **Expression Orale:** Tâche 2_{i:03d} + Tâche 3_{i:03d}\n"
        index_content += f"- **Expression Écrite:** Tâche 1_{i:03d} + Tâche 2_{i:03d} + Tâche 3_{i:03d}\n\n"
    
    index_content += f"""## 📋 Structure de chaque examen

Chaque examen contient :

### 🗣️ Expression Orale (EO) - 12 minutes total
- **Tâche 2** : Conversation simulée (5-7 minutes)
- **Tâche 3** : Monologue suivi (4-5 minutes)

### ✍️ Expression Écrite (EE) - 60 minutes total
- **Tâche 1** : Message personnel (60-120 mots, 15 minutes)
- **Tâche 2** : Article de blog (120-150 mots, 20 minutes)
- **Tâche 3** : Essai argumentatif (120-180 mots, 25 minutes)

## 🎯 Guide d'utilisation

### 📝 Préparation
1. **Choisissez un examen** dans la liste ci-dessus
2. **Préparez votre environnement** (chronomètre, papier, stylo)
3. **Lisez les instructions** de chaque tâche attentivement

### ⏱️ Passage de l'examen
1. **Expression Orale** : Suivez les liens vers les tâches 2 et 3
2. **Expression Écrite** : Respectez les temps et limites de mots
3. **Chronométrez-vous** pour simuler les conditions réelles

### 📊 Évaluation
- **Adéquation** du discours à la situation
- **Capacité** à présenter et défendre un point de vue  
- **Cohérence** et cohésion du discours
- **Lexique** et morphosyntaxe

## 🔄 Régénération

Pour créer de nouveaux examens ou modifier le nombre d'examens :
```bash
python3 exam_generator.py
```

---

📈 **Statistiques :** {num_exams} examens complets générés automatiquement  
🔗 **Navigation :** [← Retour au README principal](../README.md)

*Bonne chance pour vos examens ! 🍀*
"""
    
    index_file = output_dir / 'README.md'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"  ✓ Created enhanced index file: {index_file.name}")


def update_main_readme(base_path: Path, num_exams: int) -> None:
    """
    Update the main README.md file to include a link to the complete exams.
    """
    
    readme_path = base_path / 'README.md'
    
    if not readme_path.exists():
        print("⚠️  Main README.md not found, skipping update")
        return
    
    # Read current README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if complete exams section already exists
    complete_exams_marker = "### Examens Complets"
    
    if complete_exams_marker in content:
        print("📝 Complete exams section already exists in README, updating...")
        # Find and replace the existing section
        lines = content.split('\n')
        start_idx = None
        end_idx = None
        
        for i, line in enumerate(lines):
            if line.strip() == complete_exams_marker:
                start_idx = i
            elif start_idx is not None and line.startswith('###') and i > start_idx:
                end_idx = i
                break
        
        if start_idx is not None:
            if end_idx is None:
                end_idx = len(lines)
            
            # Replace the section
            new_section = generate_complete_exams_section(num_exams)
            lines[start_idx:end_idx] = new_section.split('\n')
            content = '\n'.join(lines)
    else:
        print("📝 Adding complete exams section to README...")
        # Add the section after "## TCF Canada"
        tcf_canada_marker = "## TCF Canada"
        
        if tcf_canada_marker in content:
            # Insert after the TCF Canada header
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() == tcf_canada_marker:
                    # Insert the complete exams section after the TCF Canada header
                    new_section = "\n" + generate_complete_exams_section(num_exams) + "\n"
                    lines.insert(i + 1, new_section)
                    break
            content = '\n'.join(lines)
        else:
            print("⚠️  Could not find '## TCF Canada' section in README")
            return
    
    # Write the updated content
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Updated main README.md with link to complete exams")


def generate_complete_exams_section(num_exams: int) -> str:
    """
    Generate the complete exams section for the main README.
    """
    
    section = f"""### Examens Complets

🎯 **Examens complets TCF Canada** - Chaque examen contient toutes les tâches (EO + EE) avec sélection séquentielle des sujets.

📚 **[Accéder aux examens complets](tcf_complete_exams/README.md)** - {num_exams} examens disponibles

**Structure de chaque examen :**
- **Expression Orale :** Tâche 2 (conversation) + Tâche 3 (monologue)  
- **Expression Écrite :** Tâche 1 (message) + Tâche 2 (article) + Tâche 3 (essai)"""
    
    return section


def main():
    """Main function."""
    
    # Get the base path (where the script is located)
    base_path = Path(__file__).parent
    
    # Ask user for number of exams (with fallback for non-interactive mode)
    try:
        user_input = input("Combien d'examens voulez-vous générer ? (par défaut: 10): ") or "10"
        num_exams = int(user_input)
        if num_exams <= 0:
            num_exams = 10
    except (ValueError, EOFError):
        # Default to 10 exams if input fails or in non-interactive mode
        num_exams = 10
        print("Mode non-interactif détecté. Génération de 10 examens par défaut.")
    
    # Create the complete exams
    create_complete_exams(base_path, num_exams)


if __name__ == "__main__":
    main()
