"""
Record Analyzer Module
======================

OOP Concepts:
- Single Responsibility: Focused on analyzing sequence records
- Composition: Works with SeqRecord objects (uses Bio objects)
- Method organization: Related analysis functions grouped in a class

This module provides analysis capabilities for biological sequence records.
"""

from typing import List, Dict, Any, Optional
from Bio.SeqRecord import SeqRecord
from collections import Counter


class RecordAnalyzer:
    """
    Analyzes biological sequence records.
    
    OOP Principles:
    - Groups related analysis methods together
    - Stateless design: methods don't modify internal state
    - Can be extended with inheritance for specialized analyzers
    
    This class can work with individual records or collections of records.
    """
    
    def __init__(self):
        """
        Initialize the analyzer.
        
        Note: This class is currently stateless (no attributes).
        It groups related analysis methods together for organization.
        """
        pass
    
    def get_basic_info(self, record: SeqRecord) -> Dict[str, Any]:
        """
        Extract basic information from a sequence record.
        
        Args:
            record: BioPython SeqRecord object
            
        Returns:
            Dictionary with basic record information
            
        Example:
            >>> analyzer = RecordAnalyzer()
            >>> info = analyzer.get_basic_info(record)
            >>> print(info['id'], info['length'])
        """
        return {
            'id': record.id,
            'name': record.name,
            'description': record.description,
            'length': len(record.seq),
            'sequence_type': self._guess_sequence_type(record.seq),
        }
    
    def _guess_sequence_type(self, seq) -> str:
        """
        Guess if sequence is DNA, RNA, or protein.
        
        OOP Concept: Private helper method
        - Implementation detail, not part of public API
        - Can be changed without affecting users of the class
        
        Args:
            seq: Bio.Seq object
            
        Returns:
            'DNA', 'RNA', 'protein', or 'unknown'
        """
        seq_str = str(seq).upper()
        if not seq_str:
            return 'unknown'
        
        # Check for RNA
        if 'U' in seq_str and 'T' not in seq_str:
            return 'RNA'
        
        # Check for DNA (ATCG)
        dna_chars = set('ATCGN')
        if all(c in dna_chars for c in seq_str):
            return 'DNA'
        
        # Probably protein
        return 'protein'
    
    def calculate_gc_content(self, record: SeqRecord) -> float:
        """
        Calculate GC content percentage for nucleotide sequences.
        
        Args:
            record: SeqRecord object
            
        Returns:
            GC content as percentage (0-100)
            
        Raises:
            ValueError: If sequence is not DNA/RNA
        """
        seq_type = self._guess_sequence_type(record.seq)
        if seq_type not in ['DNA', 'RNA']:
            raise ValueError(f"GC content only applicable to DNA/RNA, not {seq_type}")
        
        seq_str = str(record.seq).upper()
        gc_count = seq_str.count('G') + seq_str.count('C')
        total = len(seq_str)
        
        return (gc_count / total * 100) if total > 0 else 0.0
    
    def get_nucleotide_composition(self, record: SeqRecord) -> Dict[str, int]:
        """
        Count nucleotides in the sequence.
        
        Args:
            record: SeqRecord object
            
        Returns:
            Dictionary mapping nucleotide to count
        """
        return dict(Counter(str(record.seq).upper()))
    
    def extract_features(self, record: SeqRecord) -> List[Dict[str, Any]]:
        """
        Extract feature annotations from a record.
        
        Features include genes, CDS, regulatory regions, etc.
        
        Args:
            record: SeqRecord with features
            
        Returns:
            List of feature dictionaries
            
        Example:
            >>> features = analyzer.extract_features(record)
            >>> for feat in features:
            ...     print(feat['type'], feat['location'])
        """
        features_list = []
        
        for feature in record.features:
            feat_dict = {
                'type': feature.type,
                'location': str(feature.location),
                'strand': feature.location.strand,
                'qualifiers': dict(feature.qualifiers)
            }
            features_list.append(feat_dict)
        
        return features_list
    
    def get_gene_names(self, record: SeqRecord) -> List[str]:
        """
        Extract gene names from record features.
        
        Args:
            record: SeqRecord object
            
        Returns:
            List of unique gene names found
        """
        gene_names = set()
        
        for feature in record.features:
            # Check different possible qualifier keys
            if 'gene' in feature.qualifiers:
                gene_names.update(feature.qualifiers['gene'])
            if 'gene_synonym' in feature.qualifiers:
                gene_names.update(feature.qualifiers['gene_synonym'])
        
        return sorted(gene_names)
    
    def filter_by_length(
        self, 
        records: List[SeqRecord], 
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> List[SeqRecord]:
        """
        Filter records by sequence length.
        
        OOP Concept: Method that operates on collections
        - Shows how a class can work with both single items and collections
        
        Args:
            records: List of SeqRecord objects
            min_length: Minimum sequence length (inclusive)
            max_length: Maximum sequence length (inclusive)
            
        Returns:
            Filtered list of records
            
        Example:
            >>> filtered = analyzer.filter_by_length(records, min_length=1000, max_length=5000)
        """
        filtered = records
        
        if min_length is not None:
            filtered = [r for r in filtered if len(r.seq) >= min_length]
        
        if max_length is not None:
            filtered = [r for r in filtered if len(r.seq) <= max_length]
        
        return filtered
    
    def compare_records(self, records: List[SeqRecord]) -> Dict[str, Any]:
        """
        Compare multiple records and generate summary statistics.
        
        Args:
            records: List of SeqRecord objects
            
        Returns:
            Dictionary with comparison statistics
            
        Example:
            >>> stats = analyzer.compare_records(records)
            >>> print(f"Average length: {stats['avg_length']}")
        """
        if not records:
            return {}
        
        lengths = [len(r.seq) for r in records]
        
        return {
            'total_records': len(records),
            'avg_length': sum(lengths) / len(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'total_bases': sum(lengths),
            'unique_organisms': len(set(
                r.annotations.get('organism', 'Unknown') 
                for r in records
            ))
        }
    
    def get_organism(self, record: SeqRecord) -> str:
        """
        Extract organism name from record annotations.
        
        Args:
            record: SeqRecord object
            
        Returns:
            Organism name or 'Unknown'
        """
        return record.annotations.get('organism', 'Unknown')
    
    def search_features_by_type(
        self, 
        record: SeqRecord, 
        feature_type: str
    ) -> List[Any]:
        """
        Find all features of a specific type.
        
        Args:
            record: SeqRecord object
            feature_type: Type of feature (e.g., 'gene', 'CDS', 'exon')
            
        Returns:
            List of features matching the type
            
        Example:
            >>> genes = analyzer.search_features_by_type(record, 'gene')
        """
        return [f for f in record.features if f.type == feature_type]
    
    def __repr__(self) -> str:
        """String representation."""
        return "RecordAnalyzer()"
