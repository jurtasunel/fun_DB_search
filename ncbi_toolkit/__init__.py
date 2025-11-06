"""
NCBI Toolkit Package
====================

A package for interacting with NCBI databases using Biopython's Entrez module.

This package demonstrates Object-Oriented Programming principles:
- Encapsulation: Data and methods bundled in classes
- Abstraction: Complex operations hidden behind simple interfaces
- Single Responsibility: Each class has one clear purpose
- Composition: Classes work together to achieve complex tasks

Main Components:
- EntrezClient: Handles connections to NCBI databases
- RecordAnalyzer: Analyzes and processes sequence records
- RecordExporter: Exports records in various formats
- config: Configuration management
"""

from .entrez_client import EntrezClient
from .record_analyzer import RecordAnalyzer
from .record_exporter import RecordExporter

__version__ = "1.0.0"
__all__ = ["EntrezClient", "RecordAnalyzer", "RecordExporter"]
