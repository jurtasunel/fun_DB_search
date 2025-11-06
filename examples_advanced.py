"""
Advanced Example: Custom Workflow
==================================

This example shows more advanced OOP concepts and custom workflows.

OOP Concepts:
- Inheritance: Creating specialized classes
- Method overriding: Customizing behavior
- Class composition: Objects working together
"""

from ncbi_toolkit import EntrezClient, RecordAnalyzer, RecordExporter
from ncbi_toolkit.config import NCBIConfig
from typing import List
from Bio.SeqRecord import SeqRecord


class ProteinAnalyzer(RecordAnalyzer):
    """
    Specialized analyzer for protein sequences.
    
    OOP Concept: INHERITANCE
    - Extends RecordAnalyzer base class
    - Inherits all base methods
    - Adds protein-specific functionality
    
    This demonstrates how to extend the toolkit for specific needs.
    """
    
    def calculate_molecular_weight(self, record: SeqRecord) -> float:
        """
        Estimate molecular weight of protein sequence.
        
        OOP Concept: NEW METHOD in child class
        - Adds functionality not in parent class
        
        Args:
            record: Protein sequence record
            
        Returns:
            Approximate molecular weight in Daltons
        """
        # Simplified average weight per amino acid
        avg_weight_per_aa = 110  # Daltons
        return len(record.seq) * avg_weight_per_aa
    
    def count_amino_acids(self, record: SeqRecord) -> dict:
        """
        Count amino acids in protein sequence.
        
        Args:
            record: Protein sequence record
            
        Returns:
            Dictionary of amino acid counts
        """
        from collections import Counter
        return dict(Counter(str(record.seq).upper()))
    
    def get_basic_info(self, record: SeqRecord) -> dict:
        """
        Override parent method to add protein-specific info.
        
        OOP Concept: METHOD OVERRIDING
        - Calls parent method (super())
        - Adds additional information
        - Maintains same interface
        
        Args:
            record: SeqRecord object
            
        Returns:
            Extended basic info dictionary
        """
        # Call parent method first
        info = super().get_basic_info(record)
        
        # Add protein-specific information
        if info['sequence_type'] == 'protein':
            info['molecular_weight'] = self.calculate_molecular_weight(record)
            info['amino_acid_composition'] = self.count_amino_acids(record)
        
        return info


class ResearchWorkflow:
    """
    Orchestrates a complete research workflow.
    
    OOP Concept: COMPOSITION
    - Uses multiple objects (client, analyzer, exporter)
    - Coordinates their interactions
    - Encapsulates complex multi-step processes
    
    This is a higher-level class that uses other classes.
    """
    
    def __init__(self, config: NCBIConfig, output_dir: str = "research_output"):
        """
        Initialize the workflow with all necessary components.
        
        Args:
            config: NCBI configuration
            output_dir: Directory for results
        """
        self.client = EntrezClient(config)
        self.analyzer = RecordAnalyzer()
        self.protein_analyzer = ProteinAnalyzer()
        self.exporter = RecordExporter(output_dir)
    
    def run_gene_search(
        self, 
        gene_name: str, 
        organism: str,
        max_results: int = 20
    ) -> List[SeqRecord]:
        """
        Search for a gene in a specific organism.
        
        OOP Concept: HIGH-LEVEL METHOD
        - Combines multiple operations
        - Provides domain-specific interface
        - Hides implementation complexity
        
        Args:
            gene_name: Name of gene to search
            organism: Scientific name of organism
            max_results: Maximum results to retrieve
            
        Returns:
            List of sequence records
        """
        print(f"\n🔍 Searching for '{gene_name}' in '{organism}'...")
        
        # Build search query
        term = f'{gene_name}[Gene name] AND "{organism}"[Organism]'
        
        # Search and fetch
        records = self.client.search_and_fetch(
            database="nucleotide",
            term=term,
            max_results=max_results
        )
        
        print(f"✓ Found {len(records)} records")
        return records
    
    def analyze_and_export(
        self,
        records: List[SeqRecord],
        project_name: str
    ) -> dict:
        """
        Analyze records and export results.
        
        Args:
            records: List of sequence records
            project_name: Name for output files
            
        Returns:
            Dictionary with analysis results and file paths
        """
        print(f"\n📊 Analyzing {len(records)} records...")
        
        # Perform analysis
        comparison = self.analyzer.compare_records(records)
        
        print(f"✓ Analysis complete")
        print(f"  Average length: {comparison['avg_length']:.0f} bp")
        print(f"  Total sequences: {comparison['total_records']}")
        
        # Export results
        print(f"\n💾 Exporting results...")
        exported = self.exporter.export_multiple_formats(
            records=records,
            base_filename=project_name,
            formats=['fasta', 'csv', 'summary', 'json']
        )
        
        print(f"✓ Exported {len(exported)} files")
        
        return {
            'analysis': comparison,
            'files': exported,
            'record_count': len(records)
        }
    
    def run_comparative_study(
        self,
        gene_name: str,
        organisms: List[str],
        max_per_organism: int = 10
    ):
        """
        Compare a gene across multiple organisms.
        
        OOP Concept: WORKFLOW METHOD
        - Orchestrates complex multi-step process
        - Demonstrates class coordination
        
        Args:
            gene_name: Gene to compare
            organisms: List of organism names
            max_per_organism: Max sequences per organism
        """
        print("=" * 80)
        print(f"COMPARATIVE STUDY: {gene_name} across {len(organisms)} organisms")
        print("=" * 80)
        
        all_records = []
        
        for organism in organisms:
            records = self.run_gene_search(gene_name, organism, max_per_organism)
            all_records.extend(records)
        
        # Analyze combined dataset
        result = self.analyze_and_export(
            records=all_records,
            project_name=f"comparative_{gene_name}"
        )
        
        print("\n" + "=" * 80)
        print("STUDY COMPLETE")
        print("=" * 80)
        print(f"Total sequences analyzed: {result['record_count']}")
        print(f"Files saved to: {self.exporter.output_dir}")
        
        return result


def example_inheritance():
    """Example demonstrating inheritance with ProteinAnalyzer."""
    print("\n" + "=" * 80)
    print("EXAMPLE: Inheritance - Protein Analysis")
    print("=" * 80)
    
    config = NCBIConfig(email="your.email@example.com")
    client = EntrezClient(config)
    
    # Search for protein sequences
    print("\n🔍 Searching for insulin protein sequences...")
    records = client.search_and_fetch(
        database="protein",
        term="insulin[Protein] AND human[Organism]",
        max_results=5,
        return_type="gb"
    )
    
    # Use specialized protein analyzer
    protein_analyzer = ProteinAnalyzer()
    
    print(f"\n📊 Analyzing {len(records)} protein sequences:\n")
    for i, record in enumerate(records[:3], 1):
        info = protein_analyzer.get_basic_info(record)
        print(f"Protein {i}:")
        print(f"  ID: {info['id']}")
        print(f"  Length: {info['length']} amino acids")
        if 'molecular_weight' in info:
            print(f"  Est. molecular weight: {info['molecular_weight']:.0f} Da")
        print()


def example_workflow():
    """Example demonstrating the ResearchWorkflow class."""
    print("\n" + "=" * 80)
    print("EXAMPLE: Composition - Research Workflow")
    print("=" * 80)
    
    # Setup
    config = NCBIConfig(email="your.email@example.com")
    workflow = ResearchWorkflow(config, output_dir="workflow_results")
    
    # Run comparative study
    workflow.run_comparative_study(
        gene_name="hemoglobin",
        organisms=["Homo sapiens", "Mus musculus"],
        max_per_organism=5
    )


def main():
    """Run all examples."""
    print("\n" + "█" * 80)
    print("ADVANCED OOP EXAMPLES")
    print("█" * 80)
    
    # Example 1: Inheritance
    example_inheritance()
    
    # Example 2: Composition
    example_workflow()
    
    print("\n" + "█" * 80)
    print("ALL EXAMPLES COMPLETED")
    print("█" * 80 + "\n")


if __name__ == "__main__":
    main()
