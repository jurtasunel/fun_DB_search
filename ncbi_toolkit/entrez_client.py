"""
Entrez Client Module
====================

OOP Concepts:
- Single Responsibility: This class only handles NCBI database connections
- Abstraction: Complex API calls hidden behind simple methods
- Resource Management: Proper handle opening/closing with context managers

This module provides a high-level interface for querying NCBI databases.
"""

from typing import List, Dict, Any, Optional
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from .config import NCBIConfig


class EntrezClient:
    """
    Client for interacting with NCBI Entrez databases.
    
    This class demonstrates OOP by:
    - Encapsulating all NCBI API interaction logic
    - Managing connection state (email, api_key)
    - Providing clean, reusable methods for common operations
    
    Attributes:
        config (NCBIConfig): Configuration object with credentials
    """
    
    def __init__(self, config: NCBIConfig):
        """
        Initialize the Entrez client.
        
        OOP Concept: Dependency Injection
        - Config is passed in rather than created internally
        - Makes testing easier and code more flexible
        
        Args:
            config: NCBIConfig object with credentials
        """
        self.config = config
        self._configure_entrez()
    
    def _configure_entrez(self):
        """
        Configure Entrez module with credentials.
        
        OOP Concept: Private method (helper method)
        - Prefixed with _ to indicate internal use only
        - Separates implementation details from public interface
        """
        Entrez.email = self.config.email
        if self.config.api_key:
            Entrez.api_key = self.config.api_key
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Retrieve information about all available NCBI databases.
        
        Returns:
            Dictionary containing database metadata
            
        Example:
            >>> client = EntrezClient(config)
            >>> info = client.get_database_info()
            >>> print(info['DbList'])
        """
        with Entrez.einfo() as handle:
            record = Entrez.read(handle)
        return record
    
    def search(
        self, 
        database: str, 
        term: str, 
        max_results: int = 20,
        sort: str = "relevance"
    ) -> Dict[str, Any]:
        """
        Search an NCBI database.
        
        OOP Concept: Method parameters with defaults
        - Provides flexibility while keeping simple cases simple
        
        Args:
            database: NCBI database name (e.g., 'nucleotide', 'protein', 'sra')
            term: Search query (use NCBI syntax)
            max_results: Maximum number of results to return
            sort: Sort order ('relevance' or 'pub_date')
            
        Returns:
            Dictionary with search results including 'IdList' and 'Count'
            
        Example:
            >>> results = client.search(
            ...     database="nucleotide",
            ...     term='esxi[Gene name] AND "Mycobacterium bovis"[Organism]',
            ...     max_results=50
            ... )
            >>> print(f"Found {results['Count']} records")
        """
        with Entrez.esearch(
            db=database, 
            term=term, 
            retmax=str(max_results),
            sort=sort
        ) as handle:
            record = Entrez.read(handle)
        return record
    
    def fetch_records(
        self,
        database: str,
        id_list: List[str],
        return_type: str = "gb",
        return_mode: str = "text"
    ) -> List[SeqRecord]:
        """
        Fetch full records from NCBI database by IDs.
        
        Args:
            database: NCBI database name
            id_list: List of record IDs to fetch
            return_type: Format type ('gb', 'fasta', 'xml', etc.)
            return_mode: Return mode ('text' or 'xml')
            
        Returns:
            List of SeqRecord objects
            
        Example:
            >>> search_results = client.search("nucleotide", "hemoglobin[Protein]")
            >>> records = client.fetch_records("nucleotide", search_results['IdList'])
            >>> print(f"Fetched {len(records)} records")
        """
        if not id_list:
            return []
        
        with Entrez.efetch(
            db=database,
            id=id_list,
            rettype=return_type,
            retmode=return_mode
        ) as handle:
            records = list(SeqIO.parse(handle, return_type))
        
        return records
    
    def search_and_fetch(
        self,
        database: str,
        term: str,
        max_results: int = 20,
        return_type: str = "gb"
    ) -> List[SeqRecord]:
        """
        Convenience method: search and fetch in one call.
        
        OOP Concept: Composite method
        - Combines multiple operations into a common workflow
        - Demonstrates how objects can use their own methods
        
        Args:
            database: NCBI database name
            term: Search query
            max_results: Maximum number of results
            return_type: Format type for records
            
        Returns:
            List of SeqRecord objects
            
        Example:
            >>> records = client.search_and_fetch(
            ...     database="nucleotide",
            ...     term="insulin[Gene] AND human[Organism]",
            ...     max_results=10
            ... )
        """
        search_results = self.search(database, term, max_results)
        id_list = search_results.get('IdList', [])
        
        if not id_list:
            return []
        
        return self.fetch_records(database, id_list, return_type)
    
    def get_summary(self, database: str, id_list: List[str]) -> List[Dict]:
        """
        Get summary information for records (faster than full fetch).
        
        Args:
            database: NCBI database name
            id_list: List of record IDs
            
        Returns:
            List of summary dictionaries
            
        Example:
            >>> summaries = client.get_summary("nucleotide", ["NM_000207", "NM_000518"])
        """
        if not id_list:
            return []
        
        with Entrez.esummary(db=database, id=",".join(id_list)) as handle:
            records = Entrez.read(handle)
        
        return records if isinstance(records, list) else [records]
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"EntrezClient(email='{self.config.email}')"
