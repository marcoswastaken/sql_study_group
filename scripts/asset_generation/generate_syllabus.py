#!/usr/bin/env python3
"""
Generate syllabus markdown from structured JSON schema.

This script converts the syllabus_schema.json file into a formatted markdown syllabus.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_syllabus_schema(schema_path):
    """Load and parse the syllabus schema JSON file."""
    try:
        with open(schema_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def format_list_items(items, indent_level=0):
    """Format a list of items with proper markdown bullets."""
    if not items:
        return ""
    
    indent = "  " * indent_level
    bullet = "- "
    
    formatted_items = []
    for item in items:
        if isinstance(item, dict):
            # Handle structured items like SQLZoo/LeetCode with URLs
            if 'url' in item:
                if item['url']:
                    formatted_items.append(f"{indent}{bullet}[{item['title']}]({item['url']})")
                else:
                    formatted_items.append(f"{indent}{bullet}**{item['title']}**")
                
                # Add description if available
                if 'description' in item and item['description']:
                    formatted_items.append(f"{indent}  - {item['description']}")
            else:
                # Handle other structured items
                formatted_items.append(f"{indent}{bullet}{item.get('title', str(item))}")
        else:
            # Handle simple string items
            formatted_items.append(f"{indent}{bullet}{item}")
    
    return "\n".join(formatted_items)

def generate_week_section(week_data):
    """Generate markdown for a single week section."""
    week_num = week_data['number']
    title = week_data['title']
    
    # Start with week header
    section = f"## Week {week_num}: {title}\n\n"
    
    # Add intro if available
    if week_data.get('intro'):
        section += f"{week_data['intro']}\n\n"
    
    # Core concepts
    if week_data.get('core_concepts'):
        section += "**Core Concepts:**\n"
        section += format_list_items(week_data['core_concepts'])
        section += "\n\n"
    
    # Learning objectives
    if week_data.get('learning_objectives'):
        section += "**Learning Objectives:**\n"
        # Keep original capitalization
        section += format_list_items(week_data['learning_objectives'])
        section += "\n\n"
    
    # SQLZoo exercises
    if week_data.get('sqlzoo'):
        section += "**SQLZoo Exercises:**\n"
        section += format_list_items(week_data['sqlzoo'])
        section += "\n\n"
    
    # LeetCode practice
    if week_data.get('leetcode'):
        section += "**LeetCode Practice (Easy to Medium):**\n"
        section += format_list_items(week_data['leetcode'])
        section += "\n\n"
    
    # Additional resources
    if week_data.get('additional_resources'):
        section += "**Additional Resources:**\n"
        section += format_list_items(week_data['additional_resources'])
        section += "\n\n"
    
    # Add note if available
    if week_data.get('note'):
        section += f"**Note:** {week_data['note']}\n\n"
    
    return section

def generate_syllabus_markdown(schema_data, output_path):
    """Generate complete syllabus markdown from schema data."""
    
    # Start with title (no YAML front matter)
    markdown_content = f"# {schema_data['metadata']['title']}\n\n"
    
    # Add description if available
    if schema_data['metadata'].get('description'):
        markdown_content += f"{schema_data['metadata']['description']}\n\n"
    
    # Generate week sections
    for week in schema_data['weeks']:
        markdown_content += generate_week_section(week)
        markdown_content += "---\n\n"
    
    # Add study tips
    if schema_data.get('study_tips'):
        markdown_content += "## Study Tips\n\n"
        markdown_content += format_list_items(schema_data['study_tips'])
        markdown_content += "\n\n"
    
    # Write to file
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        print(f"Syllabus successfully generated: {output_path}")
        return True
    except Exception as e:
        print(f"Error writing syllabus file: {e}")
        return False

def main():
    """Main function to generate syllabus from schema."""
    
    # Set up paths
    project_root = Path(__file__).parent.parent.parent
    schema_path = Path(__file__).parent / "syllabus_schema.json"
    output_path = project_root / "syllabus.md"
    
    print("Generating syllabus markdown from schema...")
    print(f"Schema file: {schema_path}")
    print(f"Output file: {output_path}")
    
    # Load schema
    schema_data = load_syllabus_schema(schema_path)
    if not schema_data:
        return False
    
    # Generate markdown
    success = generate_syllabus_markdown(schema_data, output_path)
    
    if success:
        print("\n✅ Syllabus generation completed successfully!")
        print(f"📄 Generated file: {output_path}")
        
        # Show some stats
        week_count = len(schema_data['weeks'])
        print(f"📊 Stats: {week_count} weeks, "
              f"{sum(len(week.get('leetcode', [])) for week in schema_data['weeks'])} LeetCode problems, "
              f"{sum(len(week.get('sqlzoo', [])) for week in schema_data['weeks'])} SQLZoo exercises")
    else:
        print("\n❌ Syllabus generation failed!")
        return False
    
    return True

if __name__ == "__main__":
    main() 