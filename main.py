"""
Main Example Script
===================

This demonstrates how to use the ncbi_toolkit package in a real workflow.

OOP Concepts Demonstrated:
- Object instantiation and composition
- Method chaining and workflows
- Separation of concerns (config, client, analysis, export)
"""

from ncbi_toolkit import EntrezClient, RecordAnalyzer, RecordExporter
from ncbi_toolkit.config import NCBIConfig


def main():
    """
    Main workflow example: Search, analyze, and export NCBI records.
    
    This is a "script" - meant to be executed directly.
    It uses the "modules" (classes) from the ncbi_toolkit "package".
    """
    
    # Step 1: Configure credentials
    # OOP Concept: Object creation with dependency injection
    print("=" * 80)
    print("NCBI Database Search Example")
    print("=" * 80)
    print("\nStep 1: Configuration")
    
    config = NCBIConfig(
        email="your.email@example.com",  # Replace with your email
        api_key=None  # Optional: Add your API key for faster access
    )
    print(f"✓ Configured: {config}")
    
    # Step 2: Create client
    # OOP Concept: Composition - client uses config object
    print("\nStep 2: Creating NCBI client")
    client = EntrezClient(config)
    print(f"✓ Client ready: {client}")
    
    # Step 3: Search for records
    print("\nStep 3: Searching NCBI nucleotide database")
    search_term = 'esxi[Gene name] AND "Mycobacterium bovis"[Organism]'
    print(f"Query: {search_term}")
    
    # Using the search_and_fetch convenience method
    records = client.search_and_fetch(
        database="nucleotide",
        term=search_term,
        max_results=10
    )
    print(f"✓ Found and fetched {len(records)} records")
    
    # Step 4: Analyze records
    # OOP Concept: Create analyzer object
    print("\nStep 4: Analyzing records")
    analyzer = RecordAnalyzer()
    
    # Compare all records
    comparison = analyzer.compare_records(records)
    print(f"\nComparison Statistics:")
    print(f"  Total records: {comparison['total_records']}")
    print(f"  Average length: {comparison['avg_length']:.0f} bp")
    print(f"  Range: {comparison['min_length']} - {comparison['max_length']} bp")
    print(f"  Total bases: {comparison['total_bases']:,}")
    
    # Analyze individual records
    print(f"\nFirst 3 records details:")
    for i, record in enumerate(records[:3], 1):
        info = analyzer.get_basic_info(record)
        print(f"\n  Record {i}:")
        print(f"    ID: {info['id']}")
        print(f"    Length: {info['length']} bp")
        print(f"    Type: {info['sequence_type']}")
        
        # Get GC content if it's DNA/RNA
        if info['sequence_type'] in ['DNA', 'RNA']:
            gc = analyzer.calculate_gc_content(record)
            print(f"    GC content: {gc:.2f}%")
        
        # Get gene names
        genes = analyzer.get_gene_names(record)
        if genes:
            print(f"    Genes: {', '.join(genes)}")
    
    # Filter records by length
    filtered = analyzer.filter_by_length(records, min_length=1000, max_length=10000)
    print(f"\n  Records between 1000-10000 bp: {len(filtered)}")
    
    # Step 5: Export results
    # OOP Concept: Create exporter with configuration
    print("\nStep 5: Exporting results")
    exporter = RecordExporter(output_dir="results")
    print(f"✓ Exporter ready: {exporter}")
    
    # Export to multiple formats
    exported_files = exporter.export_multiple_formats(
        records=records,
        base_filename="mycobacterium_esxi",
        formats=['fasta', 'csv', 'json', 'summary']
    )
    
    print(f"\nExported files:")
    for format_name, file_path in exported_files.items():
        print(f"  {format_name:10s}: {file_path}")
    
    print("\n" + "=" * 80)
    print("Workflow completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    """
    This block runs only when the script is executed directly.
    Not when imported as a module.
    
    This is a Python best practice for scripts.
    """
    main()
