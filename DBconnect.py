### Documentation:

# Entrez: https://biopython.org/docs/1.76/api/Bio.Entrez.html
# Entrez youtube tutorial: https://www.youtube.com/watch?v=tl4xqdfIBh0&t=55s
# SeqIO documentation: https://biopython.org/wiki/SeqIO

# Search query NCBI nucleotide: https://www.ncbi.nlm.nih.gov/nucleotide/advanced?
# Search query SRA: https://www.ncbi.nlm.nih.gov/sra/advanced?

# SRA toolkit step-by-step: https://github.com/ncbi/sra-tools/wiki
# SRA toolkit: https://hpc.nih.gov/apps/sratoolkit.html
# SRA tools github: https://github.com/ncbi/sra-tools


### Libraries
from Bio import Entrez, SeqIO # NCBI access.

### Entrez inputs
print(Entrez)
Entrez.email = "xxxx@mail.com"
Entrez.api_key = "xxxx"    

# Get info of all databases. Each connection is considered as an "Entrez" and the record is the information read from the handle.
handle = Entrez.einfo()
record = Entrez.read(handle)
handle.close()
print(f"Metadata of entrez databases: {record}")
print("\n")

# Access nucleotide database. Retmax gives the desired number of records, the default is 20.
handle = Entrez.esearch(db = "nucleotide", term = 'esxi[Gene name] AND "Mycobacterium bovis"[Organism]', retmax = "40")
record = Entrez.read(handle)
handle.close()
# Print all the items of the handle output dictionary.
print("All accessible items of the search:")
for i in record.keys():
    print(i)
print("\n")

print(f"Get how many IDs are found with the query: {record['Count']}") # same as len(record["IdList"]). This gets ALL appearances of the search. 
print(f"Print the IDs of the query: {record['IdList']}") # this gives a list of IDs, default is 20 and can be changed with retmax.
print("\n")

# Store records in a variable.
id_list = record["IdList"]
# Make new search and retrieve full records using the IDs with efetch(). Optional arguments for returning info are Rettype (gb for genebank) and Retmode. 
handle = Entrez.efetch(db = "nucleotide", id = id_list, rettype = "gb", retmode = "text")
# Parse the output with SeqIO and store it in a list.
records = list(SeqIO.parse(handle, "gb")) 
# Use this for saving seq data to files: 
#SeqIO.write(records, "out.fasta", "fasta")
handle.close()
# Print all records returned.
print(f"All records fetched:\n{records}")
print("\n")

### Access information from individual records.
# Get one of ther records by index.
print(records[0])
# Get all attributes from a record. vars(records[0]) is endless because some atributes have nested list with thousands of gene names.
# vars() returns a dictionary wth all the attributes as keys(attr name) and values (specific value). USe .keys() to get only the top level attributes.
for attr in vars(records[0]).keys():
    print(f"Attribute: {attr}, type: {type(attr)}, lenght: {len(attr)}")
print("\n")

# Loop through all the records and access some info.
for record in records:
    print(record.name, record.seq[0:10], len(record.seq), record.description)








### SRA example
# handle = Entrez.esearch(db = "sra", term = "SRR390728")
# record = Entrez.read(handle)
# handle = Entrez.efetch(db = "sra", id = "SRR390728", rettype = "runinfo", retmode = "text")
# metadata = handle.read()
# handle.close()
# print(metadata)
