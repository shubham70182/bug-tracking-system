"""
Bug Tracking System — simple CLI
Log bugs, auto-classify category/severity using a basic ML model,
and view/filter logged bugs. Built with Python + SQLite.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import init_db, add_bug, get_all_bugs, get_bugs_by_status, update_status, get_bug_count_by_category
from classifier import load_classifiers, classify_bug


def print_bug(bug):
    print(f"  [{bug['id']}] {bug['title']}")
    print(f"      Category: {bug['category']} | Severity: {bug['severity']} | Status: {bug['status']}")
    print(f"      Logged: {bug['created_at']}")


def log_new_bug(category_model, severity_model):
    title = input("Bug title: ").strip()
    description = input("Description: ").strip()

    category, severity = classify_bug(description, category_model, severity_model)
    print(f"\nAuto-classified as -> Category: {category}, Severity: {severity}")
    confirm = input("Accept classification? (y/n): ").strip().lower()

    if confirm == "n":
        category = input("Enter category manually: ").strip()
        severity = input("Enter severity manually: ").strip()

    bug_id = add_bug(title, description, category, severity)
    print(f"Bug #{bug_id} logged successfully.\n")


def view_bugs():
    status_filter = input("Filter by status (Open/In Progress/Resolved) or press Enter for all: ").strip()
    bugs = get_bugs_by_status(status_filter) if status_filter else get_all_bugs()

    if not bugs:
        print("No bugs found.\n")
        return

    print(f"\n{len(bugs)} bug(s) found:")
    for bug in bugs:
        print_bug(bug)
    print()


def change_status():
    bug_id = input("Bug ID to update: ").strip()
    new_status = input("New status (Open/In Progress/Resolved): ").strip()
    update_status(int(bug_id), new_status)
    print(f"Bug #{bug_id} status updated to '{new_status}'.\n")


def show_summary():
    counts = get_bug_count_by_category()
    if not counts:
        print("No bugs logged yet.\n")
        return
    print("\nBug count by category:")
    for cat, count in counts.items():
        print(f"  {cat}: {count}")
    print()


def main():
    init_db()
    category_model, severity_model = load_classifiers()

    menu = """
Bug Tracking System
====================
1. Log a new bug
2. View bugs
3. Update bug status
4. Summary by category
5. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            log_new_bug(category_model, severity_model)
        elif choice == "2":
            view_bugs()
        elif choice == "3":
            change_status()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option, try again.\n")


if __name__ == "__main__":
    main()
