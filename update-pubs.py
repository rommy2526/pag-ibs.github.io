import requests
from datetime import datetime

# List to store the publications
publications = []

# Get the current date and time
now = datetime.now()
date_string = now.strftime("%Y-%m-%d %H:%M:%S")

# Open the input file and read the DOIs
with open("publication-dois.txt", "r") as file:
 for i, line in enumerate(file, start=1):
    # Skip comments
    if line.startswith('#'):
        continue

    # Remove trailing newline character
    doi = line.strip().replace('http://dx.doi.org/', '')

    # Fetch the publication details from the Crossref API
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)

    # Check the status of the response
    if response.status_code == 404:
        print(f"Line {i}: DOI {doi} not found.")
        continue

    data = response.json()['message']

    # Extract the title and authors
    title = '**' + data['title'][0] + '**'  # make title bold
    authors = ", ".join([author['family'] + ', ' + author['given'] for author in data['author']])

    # Format the details into a markdown list item
    publication = f"- {title}, {authors}, [{doi}](https://doi.org/{doi})"

    # Append the list item to the list of publications
    publications.append(publication)

# Prepare the frontmatter
frontmatter = f"""---
title: Publications
date: {date_string}
---"""

# Write the frontmatter and the list of publications to a markdown file
with open("content/publications.md", "w") as file:
 file.write(frontmatter + "\n")
 for publication in publications:
    file.write(publication + "\n")
