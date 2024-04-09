import csv
import re



"""
This script handles ebscohosts generic bibliographic management format with specific tags changed according to below AISeL export format tags which this script was initially designed for:
TI- -> %T
JN- -> %B
AU- -> %A
PT- -> %0
PG- -> %P
PD- -> %D (will get split into %D, %V, %N in .csv processing steps)
UR- -> %U
AB- -> %X
"""



def parse_txt_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    entry = {}
    num_entries = 0 
    for line in lines:
        raw_line = line.strip()
        if raw_line.startswith('%'):
            key, value = raw_line[1:].split(' ', 1)
            if key == 'T':
                num_entries +=1
                print(num_entries)
                entry[key] = value.strip()


            elif key == 'A':

                #strip numbers and email-adresses from author names
                value = strip_number_and_email(value)
                # Append authors with proper formatting to handle multiple authors
                authors = value.strip().split(', ')
                formatted_authors = ', '.join([author.strip() for author in authors])
                entry[key] = entry.get(key, '') + '; ' + formatted_authors if entry.get(key, '') else formatted_authors

            elif key == 'X':
                # Append abstracts with proper formatting to handle multilines
                abstracts = value.strip().split(', ')
                formatted_abstract = ', '.join([line.strip() for line in abstracts])
                entry[key] = entry.get(key, '') + '; ' + formatted_abstract if entry.get(key, '') else formatted_abstract
            
            else:
                entry[key] = value.strip()

        # handle unconverted tags (everything not starting with %) to be ommitted from conversion 
        elif raw_line !='' and raw_line[0].isalnum:
            pass
        else:
            data.append(entry)
            entry = {}
        
    # Write to CSV
    fieldnames = ['ShortList', 'Title', 'Abstract', 'Authors', 'Journal', 'Publication Date',  'Volume', 'Issue', 'Pages', 'URL', 'Document Type']
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            # Handle 
            authors = entry.get('A', [])
            entry['Authors'] = authors if authors else ''
            abstracts = entry.get('X', [])
            entry['Abstract'] = abstracts if abstracts else ''
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
                'Abstract': entry.get('Abstract', '')
            })



#used to strip numbers and email-adresses from author strings specific to ebscohost exports
def strip_number_and_email(s):
    # Define regular expressions for matching numbers and email addresses
    number_pattern = re.compile(r'\b\d+\b')  # Matches any sequence of digits
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')  # Matches email addresses
    # Remove numbers and email addresses from the string
    s_without_number = re.sub(number_pattern, '', s)
    s_without_email = re.sub(email_pattern, '', s_without_number)

    return s_without_email.strip()

parse_txt_to_csv(r'D:\Uni\MA\LitRev\ebscohost-08-03_639hits.txt', r'D:\Uni\MA\LitRev\ebscoextract.csv')
