import csv

def parse_txt_to_csv(input_file, output_file):
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
                print((formatted_authors))

                entry[key] = entry.get(key, '') + '; ' + formatted_authors if entry.get(key, '') else formatted_authors
            # elif key == "X": return
            else:
                entry[key] = value.strip()
        else:
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

# Example usage:
parse_txt_to_csv(r'D:\Uni\MA\LitRev\aiselexp.txt', r'D:\Uni\MA\LitRev\aiselexp.csv')
