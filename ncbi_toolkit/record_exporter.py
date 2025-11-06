"""
Record Exporter Module
======================

OOP Concepts:
- Single Responsibility: Focused solely on exporting/saving records
- Abstraction: Hides file I/O complexity behind simple methods
- Extensibility: Easy to add new export formats

This module handles exporting sequence records to various file formats.
"""

from typing import List, Optional, Dict
from pathlib import Path
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import json


class RecordExporter:
    """
    Exports biological sequence records to various formats.
    
    OOP Principles:
    - Encapsulates file writing logic
    - Provides consistent interface for different formats
    - Handles file path management
    
    Attributes:
        output_dir (Path): Default directory for output files
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the exporter.
        
        OOP Concept: Constructor with default values
        - Provides sensible defaults while allowing customization
        
        Args:
            output_dir: Directory where files will be saved
        """
        self.output_dir = Path(output_dir)
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """
        Create output directory if it doesn't exist.
        
        OOP Concept: Private helper method
        - Internal implementation detail
        - Ensures object is in valid state after construction
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_fasta(
        self, 
        records: List[SeqRecord], 
        filename: str,
        output_dir: Optional[str] = None
    ) -> Path:
        """
        Export records to FASTA format.
        
        FASTA is the most common format for sequence data.
        
        Args:
            records: List of SeqRecord objects
            filename: Output filename (without extension)
            output_dir: Optional override for output directory
            
        Returns:
            Path to the created file
            
        Example:
            >>> exporter = RecordExporter("my_results")
            >>> path = exporter.export_fasta(records, "mycobacterium_sequences")
            >>> print(f"Saved to {path}")
        """
        output_path = self._get_output_path(filename, ".fasta", output_dir)
        
        with open(output_path, 'w') as f:
            SeqIO.write(records, f, "fasta")
        
        return output_path
    
    def export_genbank(
        self,
        records: List[SeqRecord],
        filename: str,
        output_dir: Optional[str] = None
    ) -> Path:
        """
        Export records to GenBank format.
        
        GenBank format includes annotations and features.
        
        Args:
            records: List of SeqRecord objects
            filename: Output filename (without extension)
            output_dir: Optional override for output directory
            
        Returns:
            Path to the created file
        """
        output_path = self._get_output_path(filename, ".gb", output_dir)
        
        with open(output_path, 'w') as f:
            SeqIO.write(records, f, "genbank")
        
        return output_path
    
    def export_csv(
        self,
        records: List[SeqRecord],
        filename: str,
        output_dir: Optional[str] = None,
        include_sequence: bool = False
    ) -> Path:
        """
        Export record metadata to CSV format.
        
        Useful for importing into Excel or data analysis tools.
        
        Args:
            records: List of SeqRecord objects
            filename: Output filename (without extension)
            output_dir: Optional override for output directory
            include_sequence: Whether to include full sequence in CSV
            
        Returns:
            Path to the created file
            
        Example:
            >>> path = exporter.export_csv(records, "sequence_info", include_sequence=False)
        """
        import csv
        
        output_path = self._get_output_path(filename, ".csv", output_dir)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            header = ['ID', 'Name', 'Description', 'Length', 'Organism']
            if include_sequence:
                header.append('Sequence')
            writer.writerow(header)
            
            # Write data
            for record in records:
                row = [
                    record.id,
                    record.name,
                    record.description,
                    len(record.seq),
                    record.annotations.get('organism', 'Unknown')
                ]
                if include_sequence:
                    row.append(str(record.seq))
                writer.writerow(row)
        
        return output_path
    
    def export_json(
        self,
        records: List[SeqRecord],
        filename: str,
        output_dir: Optional[str] = None,
        include_features: bool = True
    ) -> Path:
        """
        Export records to JSON format.
        
        Useful for web applications and data interchange.
        
        Args:
            records: List of SeqRecord objects
            filename: Output filename (without extension)
            output_dir: Optional override for output directory
            include_features: Whether to include feature annotations
            
        Returns:
            Path to the created file
        """
        output_path = self._get_output_path(filename, ".json", output_dir)
        
        data = []
        for record in records:
            record_dict = {
                'id': record.id,
                'name': record.name,
                'description': record.description,
                'sequence': str(record.seq),
                'length': len(record.seq),
                'annotations': {
                    k: v for k, v in record.annotations.items() 
                    if isinstance(v, (str, int, float, bool))
                }
            }
            
            if include_features:
                record_dict['features'] = [
                    {
                        'type': f.type,
                        'location': str(f.location),
                        'qualifiers': {
                            k: v for k, v in f.qualifiers.items()
                            if isinstance(v, (list, str))
                        }
                    }
                    for f in record.features
                ]
            
            data.append(record_dict)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def export_summary_report(
        self,
        records: List[SeqRecord],
        filename: str,
        output_dir: Optional[str] = None
    ) -> Path:
        """
        Generate a human-readable text summary report.
        
        Args:
            records: List of SeqRecord objects
            filename: Output filename (without extension)
            output_dir: Optional override for output directory
            
        Returns:
            Path to the created file
        """
        output_path = self._get_output_path(filename, ".txt", output_dir)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"SEQUENCE RECORDS SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total Records: {len(records)}\n\n")
            
            for i, record in enumerate(records, 1):
                f.write(f"\nRecord {i}:\n")
                f.write(f"  ID: {record.id}\n")
                f.write(f"  Name: {record.name}\n")
                f.write(f"  Description: {record.description}\n")
                f.write(f"  Length: {len(record.seq)} bp\n")
                f.write(f"  Organism: {record.annotations.get('organism', 'Unknown')}\n")
                f.write(f"  Features: {len(record.features)}\n")
                
                if record.seq:
                    f.write(f"  Sequence preview: {str(record.seq)[:50]}...\n")
                
                f.write("-" * 80 + "\n")
        
        return output_path
    
    def _get_output_path(
        self,
        filename: str,
        extension: str,
        output_dir: Optional[str] = None
    ) -> Path:
        """
        Construct full output file path.
        
        OOP Concept: Private helper method
        - Centralizes path construction logic
        - Ensures consistent behavior across export methods
        
        Args:
            filename: Base filename
            extension: File extension (with dot)
            output_dir: Optional directory override
            
        Returns:
            Full Path object
        """
        directory = Path(output_dir) if output_dir else self.output_dir
        directory.mkdir(parents=True, exist_ok=True)
        
        # Add extension if not present
        if not filename.endswith(extension):
            filename += extension
        
        return directory / filename
    
    def export_multiple_formats(
        self,
        records: List[SeqRecord],
        base_filename: str,
        formats: List[str] = None,
        output_dir: Optional[str] = None
    ) -> Dict[str, Path]:
        """
        Export records to multiple formats at once.
        
        OOP Concept: Composite method
        - Uses other methods of the class
        - Demonstrates code reuse within a class
        
        Args:
            records: List of SeqRecord objects
            base_filename: Base name for all files
            formats: List of formats ('fasta', 'genbank', 'csv', 'json', 'summary')
            output_dir: Optional directory override
            
        Returns:
            Dictionary mapping format name to output path
            
        Example:
            >>> paths = exporter.export_multiple_formats(
            ...     records, 
            ...     "my_sequences",
            ...     formats=['fasta', 'csv', 'summary']
            ... )
            >>> print(paths['fasta'])
        """
        if formats is None:
            formats = ['fasta', 'csv', 'summary']
        
        results = {}
        
        for fmt in formats:
            if fmt == 'fasta':
                results['fasta'] = self.export_fasta(records, base_filename, output_dir)
            elif fmt == 'genbank':
                results['genbank'] = self.export_genbank(records, base_filename, output_dir)
            elif fmt == 'csv':
                results['csv'] = self.export_csv(records, base_filename, output_dir)
            elif fmt == 'json':
                results['json'] = self.export_json(records, base_filename, output_dir)
            elif fmt == 'summary':
                results['summary'] = self.export_summary_report(records, base_filename, output_dir)
        
        return results
    
    def __repr__(self) -> str:
        """String representation."""
        return f"RecordExporter(output_dir='{self.output_dir}')"
