"""
Simple Quick-Start Examples
============================

Simple, focused examples for learning OOP basics.
Start here before moving to advanced examples.
"""

from ncbi_toolkit import EntrezClient, RecordAnalyzer, RecordExporter
from ncbi_toolkit.config import NCBIConfig


def example_1_basic_search():
    """
    Example 1: Basic search and retrieval
    
    OOP Concepts:
    - Creating objects (instantiation)
    - Calling methods
    - Object attributes
    """
    print("=" * 60)
    print("Example 1: Basic Search")
    print("=" * 60)
    
    # Create configuration object
    config = NCBIConfig(email="your.email@example.com")
    
    # Create client object using the config
    client = EntrezClient(config)
    
    # Call a method on the client object
    records = client.search_and_fetch(
        database="nucleotide",
        term="insulin[Gene] AND human[Organism]",
        max_results=5
    )
    
    # Use the results
    print(f"✓ Retrieved {len(records)} records\n")
    for i, record in enumerate(records, 1):
        print(f"  {i}. {record.id}: {record.description[:60]}...")
    
    print()


def example_2_analyzing_records():
    """
    Example 2: Analyzing sequence records
    
    OOP Concepts:
    - Using multiple objects together
    - Method chaining
    - Encapsulation (methods hide complexity)
    """
    print("=" * 60)
    print("Example 2: Analyzing Records")
    print("=" * 60)
    
    # Get some records first
    config = NCBIConfig(email="your.email@example.com")
    client = EntrezClient(config)
    records = client.search_and_fetch(
        database="nucleotide",
        term="hemoglobin[Protein] AND mouse[Organism]",
        max_results=3
    )
    
    # Create analyzer object
    analyzer = RecordAnalyzer()
    
    # Use analyzer methods
    for record in records:
        info = analyzer.get_basic_info(record)
        print(f"\n{info['id']}:")
        print(f"  Length: {info['length']} bp")
        print(f"  Type: {info['sequence_type']}")
        
        # Only calculate GC for DNA/RNA
        if info['sequence_type'] in ['DNA', 'RNA']:
            gc = analyzer.calculate_gc_content(record)
            print(f"  GC%: {gc:.2f}")
    
    # Get comparison statistics
    stats = analyzer.compare_records(records)
    print(f"\nSummary:")
    print(f"  Total records: {stats['total_records']}")
    print(f"  Average length: {stats['avg_length']:.0f} bp")
    print()


def example_3_exporting_data():
    """
    Example 3: Exporting data to files
    
    OOP Concepts:
    - Object configuration (constructor parameters)
    - Method return values
    - Object state (output_dir attribute)
    """
    print("=" * 60)
    print("Example 3: Exporting Data")
    print("=" * 60)
    
    # Get some records
    config = NCBIConfig(email="your.email@example.com")
    client = EntrezClient(config)
    records = client.search_and_fetch(
        database="nucleotide",
        term="covid-19[All Fields]",
        max_results=3
    )
    
    # Create exporter with custom output directory
    exporter = RecordExporter(output_dir="my_data")
    
    # Export to different formats
    fasta_file = exporter.export_fasta(records, "covid_sequences")
    csv_file = exporter.export_csv(records, "covid_metadata")
    
    print(f"✓ Exported to:")
    print(f"  FASTA: {fasta_file}")
    print(f"  CSV:   {csv_file}")
    print()


def example_4_complete_workflow():
    """
    Example 4: Complete workflow
    
    OOP Concepts:
    - Object composition (objects working together)
    - Separation of concerns (each class has one job)
    - Reusability (same objects for different tasks)
    """
    print("=" * 60)
    print("Example 4: Complete Workflow")
    print("=" * 60)
    
    # Setup - create all objects we need
    config = NCBIConfig(email="your.email@example.com")
    client = EntrezClient(config)
    analyzer = RecordAnalyzer()
    exporter = RecordExporter(output_dir="complete_workflow")
    
    # Step 1: Search and retrieve
    print("\n1. Searching database...")
    records = client.search_and_fetch(
        database="nucleotide",
        term="BRCA1[Gene] AND human[Organism]",
        max_results=10
    )
    print(f"   Found {len(records)} records")
    
    # Step 2: Filter
    print("\n2. Filtering by length...")
    filtered = analyzer.filter_by_length(records, min_length=500, max_length=5000)
    print(f"   {len(filtered)} records between 500-5000 bp")
    
    # Step 3: Analyze
    print("\n3. Analyzing...")
    stats = analyzer.compare_records(filtered)
    print(f"   Average length: {stats['avg_length']:.0f} bp")
    print(f"   Range: {stats['min_length']} - {stats['max_length']} bp")
    
    # Step 4: Export
    print("\n4. Exporting results...")
    files = exporter.export_multiple_formats(
        filtered,
        "BRCA1_filtered",
        formats=['fasta', 'csv', 'summary']
    )
    print(f"   Exported {len(files)} files")
    
    print("\n✓ Workflow complete!\n")


def example_5_configuration_options():
    """
    Example 5: Different ways to configure
    
    OOP Concepts:
    - Constructor overloading (different ways to create objects)
    - Class methods (alternative constructors)
    - Properties (controlled attribute access)
    """
    print("=" * 60)
    print("Example 5: Configuration Options")
    print("=" * 60)
    
    # Method 1: Direct configuration
    print("\nMethod 1: Direct instantiation")
    config1 = NCBIConfig(
        email="user@example.com",
        api_key="your_api_key_here"
    )
    print(f"  Config: {config1}")
    
    # Method 2: From environment variables
    print("\nMethod 2: From environment (requires NCBI_EMAIL env var)")
    config2 = NCBIConfig.from_env()
    print(f"  Config: {config2}")
    
    # Method 3: Update after creation
    print("\nMethod 3: Update after creation")
    config3 = NCBIConfig(email="initial@example.com")
    config3.api_key = "new_api_key"
    print(f"  Config: {config3}")
    
    print()


def main():
    """Run all examples in sequence."""
    print("\n" + "█" * 60)
    print("NCBI TOOLKIT - QUICK START EXAMPLES")
    print("█" * 60 + "\n")
    
    example_1_basic_search()
    example_2_analyzing_records()
    example_3_exporting_data()
    example_4_complete_workflow()
    example_5_configuration_options()
    
    print("█" * 60)
    print("All examples completed!")
    print("Next: Try examples_advanced.py for inheritance and composition")
    print("█" * 60 + "\n")


if __name__ == "__main__":
    main()
