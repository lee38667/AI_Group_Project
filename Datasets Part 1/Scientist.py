import csv
import sys
from collections import deque

# Data structures
names = {}
scientists = {}
papers = {}
paper_to_scientists = {}
scientist_to_papers = {}

def load_data(directory):
    # Load scientists
    with open(f"{directory}/scientists.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scientists[row["scientist_id"]] = {
                "name": row["name"],
                "papers": set()
            }
            if row["name"] not in names:
                names[row["name"]] = {row["scientist_id"]}
            else:
                names[row["name"]].add(row["scientist_id"])

    # Load papers
    with open(f"{directory}/papers.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers[row["paper_id"]] = {
                "title": row["title"],
                "year": row["year"],
                "authors": set()
            }

    # Load authors
    with open(f"{directory}/authors.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                scientist_id = row["scientist_id"]
                paper_id = row["paper_id"]
                scientists[scientist_id]["papers"].add(paper_id)
                papers[paper_id]["authors"].add(scientist_id)

                # Build mappings
                if paper_id not in paper_to_scientists:
                    paper_to_scientists[paper_id] = set()
                paper_to_scientists[paper_id].add(scientist_id)

                if scientist_id not in scientist_to_papers:
                    scientist_to_papers[scientist_id] = set()
                scientist_to_papers[scientist_id].add(paper_id)
            except KeyError:
                continue

def neighbors_for_person(scientist_id):
    neighbors = set()
    for paper_id in scientist_to_papers.get(scientist_id, set()):
        for coauthor_id in paper_to_scientists.get(paper_id, set()):
            if coauthor_id != scientist_id:
                neighbors.add((paper_id, coauthor_id))
    return neighbors

def shortest_path(source, target):
    if source == target:
        return []

    queue = deque()
    queue.append((source, []))
    visited = set()
    visited.add(source)

    while queue:
        current, path = queue.popleft()
        for paper_id, neighbor in neighbors_for_person(current):
            if neighbor == target:
                return path + [(paper_id, neighbor)]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [(paper_id, neighbor)]))
    return None

def person_id_for_name(name):
    person_ids = list(names.get(name, set()))
    if not person_ids:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for pid in person_ids:
            print(f"ID: {pid}, Name: {scientists[pid]['name']}")
        return input("Intended ID: ").strip()
    else:
        return person_ids[0]

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python Scientist.py [directory]")
    directory = sys.argv[1]

    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source_name = input("Name: ").strip()
    source_id = person_id_for_name(source_name)
    if source_id is None:
        sys.exit("Scientist not found.")

    target_name = input("Name: ").strip()
    target_id = person_id_for_name(target_name)
    if target_id is None:
        sys.exit("Scientist not found.")

    path = shortest_path(source_id, target_id)

    if path is None:
        print("No connection found.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        current_id = source_id
        for i, (paper_id, scientist_id) in enumerate(path, 1):
            paper = papers[paper_id]
            next_name = scientists[scientist_id]["name"]
            current_name = scientists[current_id]["name"]
            print(f"{i}: {current_name} and {next_name} co-authored \"{paper['title']}\"")
            current_id = scientist_id

if __name__ == "__main__":
    main()
