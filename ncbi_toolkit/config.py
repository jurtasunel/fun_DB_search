"""
Configuration Module
====================

OOP Concept: Encapsulation
- Settings are stored in a class, keeping related data together
- Private attributes (starting with _) protect sensitive data
- Property decorators provide controlled access to attributes

This module manages NCBI API credentials and settings.
"""

import os
from typing import Optional


class NCBIConfig:
    """
    Manages NCBI Entrez API configuration settings.
    
    Attributes:
        email (str): Email address for NCBI (required by their API)
        api_key (str): Optional API key for higher request limits
        
    OOP Principles demonstrated:
    - Encapsulation: Credentials bundled with validation logic
    - Data hiding: Private attributes with public properties
    """
    
    def __init__(self, email: str, api_key: Optional[str] = None):
        """
        Initialize NCBI configuration.
        
        Args:
            email: Valid email address (required by NCBI)
            api_key: Optional API key for increased rate limits
            
        Raises:
            ValueError: If email is invalid
        """
        self.email = email  # Uses property setter for validation
        self._api_key = api_key
    
    @property
    def email(self) -> str:
        """Get email address."""
        return self._email
    
    @email.setter
    def email(self, value: str):
        """
        Set email with validation.
        
        Demonstrates: Data validation in setters (encapsulation principle)
        """
        if not value or "@" not in value:
            raise ValueError("Valid email address is required for NCBI API")
        self._email = value
    
    @property
    def api_key(self) -> Optional[str]:
        """Get API key."""
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: Optional[str]):
        """Set API key."""
        self._api_key = value
    
    @classmethod
    def from_env(cls) -> "NCBIConfig":
        """
        Create config from environment variables.
        
        OOP Concept: Class method (alternative constructor)
        - Provides different ways to instantiate the class
        - Useful for flexibility in object creation
        
        Returns:
            NCBIConfig instance
            
        Environment variables:
            NCBI_EMAIL: Email address
            NCBI_API_KEY: API key (optional)
        """
        email = os.getenv("NCBI_EMAIL", "your.email@example.com")
        api_key = os.getenv("NCBI_API_KEY")
        return cls(email=email, api_key=api_key)
    
    def __repr__(self) -> str:
        """
        String representation for debugging.
        
        OOP Concept: Special methods (dunder methods)
        - __repr__ provides developer-friendly representation
        """
        return f"NCBIConfig(email='{self.email}', api_key={'***' if self._api_key else None})"
