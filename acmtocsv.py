import csv
import re

def parse_txt_to_csv(input_file, output_file):
    bibtex_entry_list = parse_bibtex_file(r'D:\Uni\MA\LitRev\acmbibtext.bib')

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    entry = {}
    for line in lines:
        line = line.strip()
        if line.startswith('%'):
            key, value = line[1:].split(' ', 1)
            if key == 'A':
                # Append authors with proper formatting
                authors = value.strip().split(', ')
                formatted_authors = ', '.join([author.strip() for author in authors])

                entry[key] = entry.get(key, '') + '; ' + formatted_authors if entry.get(key, '') else formatted_authors
            elif key == 'U':
                url = value.strip().split(' ',1)
                entry[key] = url[0].strip()
            elif key == 'R':
                doi = value.strip().split(' ',1)
                entry[key] = doi[0].strip()    
            else:
                entry[key] = value.strip()
        else:
            entry = get_abstracts_from_bibtex(entry, bibtex_entry_list)
            # print(entry)
            data.append(entry)
            entry = {}

    # Write to CSV
    fieldnames = ['ShortList', 'Title', 'Abstract', 'Authors', 'Journal', 'Publication Date',  'Volume', 'Issue', 'Pages', 'URL', 'Document Type']
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            # Convert authors list to a string separated by commas
            authors = entry.get('A', [])
            entry['Authors'] = authors if authors else ''
            writer.writerow({
                'ShortList': '',
                'Title': entry.get('T', ''),
                'Document Type': entry.get('0', ''),
                'Authors': entry.get('Authors', ''),
                'Journal': entry.get('B', ''),
                'Publication Date': entry.get('D', ''),
                'Volume': entry.get('V', ''),
                'Issue': entry.get('N', ''),
                'Pages': entry.get('P', ''),
                'URL': entry.get('U', ''),
                'Abstract': entry.get('X', '')
            })

#Parse bibtex from file into a list of dictionaries
def parse_bibtex_file(bibtex_file):
    with open(bibtex_file, 'r', encoding='utf-8') as f:
        bibtex_content = f.read()

    # Regular expression pattern to match BibTeX entries
    pattern = r'@(\w+)\{([^,]+),\s*([^@]+)@?\s*\}'

    # Find matches in the BibTeX content
    matches = re.findall(pattern, bibtex_content)

    entries = []
    for match in matches:
        entry_type = match[0]
        citation_key = match[1]
        fields_str = match[2]
        
        # Parse fields into a dictionary
        fields = {}
        for field_match in re.finditer(r'\s*(\w+)\s*=\s*{([^{}]+)}', fields_str):
            key = field_match.group(1)
            value = field_match.group(2)
            fields[key] = value
        
        entry = {
            'entry_type': entry_type,
            'citation_key': citation_key,
            'fields': fields
        }
        entries.append(entry)

    return entries


# lookup abstract from bibtext entry list by key from doi from initial endnote reference txt parsing
def get_abstracts_from_bibtex(data, bibtex_entry_list):
    # print(data)
    for entry in bibtex_entry_list:
        if 'doi' in entry['fields'] and 'R' in data and data['R'] in entry['fields']['doi']:
            abstract = entry['fields']['abstract'] if 'abstract' in entry['fields'] else ''
            data['X'] = abstract
            return data
    return data



parse_txt_to_csv(r'D:\Uni\MA\LitRev\acmexp.txt', r'D:\Uni\MA\LitRev\acmexp.csv')
