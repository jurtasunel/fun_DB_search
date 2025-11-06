# NCBI Toolkit - Object-Oriented Programming Guide

A Python package for interacting with NCBI databases using BioPython's Entrez module, designed as a **comprehensive learning resource for Object-Oriented Programming (OOP)** concepts.

## 📚 Python Terminology Clarified

Before diving in, let's clarify some Python terms:

- **Module**: A single `.py` file (e.g., `config.py`)
- **Package**: A folder containing an `__init__.py` file and multiple modules (e.g., `ncbi_toolkit/`)
- **Script**: A module designed to be executed directly (e.g., `main.py`)

```
project/
├── ncbi_toolkit/          # ← PACKAGE (folder with __init__.py)
│   ├── __init__.py
│   ├── config.py          # ← MODULE (single .py file)
│   ├── entrez_client.py   # ← MODULE
│   └── ...
├── main.py                # ← SCRIPT (executable module)
└── examples_simple.py     # ← SCRIPT
```

## 🎯 Learning Objectives

This project teaches OOP through practical examples:

1. ✅ **Classes & Objects**: Creating and using classes
2. ✅ **Encapsulation**: Bundling data and methods together
3. ✅ **Inheritance**: Creating specialized classes from base classes
4. ✅ **Composition**: Objects working together
5. ✅ **Abstraction**: Hiding complexity behind simple interfaces
6. ✅ **Single Responsibility**: Each class has one clear purpose

## 📁 Project Structure

```
fun_DB_search/
│
├── ncbi_toolkit/              # Main package
│   ├── __init__.py            # Package initialization
│   ├── config.py              # Configuration management
│   ├── entrez_client.py       # NCBI API client
│   ├── record_analyzer.py     # Sequence analysis
│   └── record_exporter.py     # Data export functionality
│
├── main.py                    # Main workflow example
├── examples_simple.py         # Simple OOP examples (START HERE!)
├── examples_advanced.py       # Advanced OOP concepts
├── DBconnect.py              # Original procedural code (for comparison)
└── README.md                  # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install BioPython (required dependency)
pip install biopython
```

### Your First OOP Script

Create a file called `my_first_search.py`:

```python
from ncbi_toolkit import EntrezClient, RecordExporter
from ncbi_toolkit.config import NCBIConfig

# Step 1: Create a configuration object
config = NCBIConfig(email="your.email@example.com")

# Step 2: Create a client object
client = EntrezClient(config)

# Step 3: Use the client to search
records = client.search_and_fetch(
    database="nucleotide",
    term="hemoglobin[Gene] AND mouse[Organism]",
    max_results=5
)

# Step 4: Create an exporter and save results
exporter = RecordExporter(output_dir="my_results")
exporter.export_fasta(records, "hemoglobin_sequences")

print(f"✓ Downloaded {len(records)} sequences!")
```

Run it:
```bash
python my_first_search.py
```

## 📖 Learning Path

### Level 1: Understanding the Basics

**Start with: `examples_simple.py`**

Run the simple examples:
```bash
python examples_simple.py
```

This file demonstrates:
- Creating objects (instantiation)
- Calling methods
- Using multiple objects together
- Basic workflows

**Key OOP Concepts Covered:**
- **Objects are instances of classes**: Like creating a specific car from a car blueprint
- **Methods are functions inside classes**: Actions an object can perform
- **Attributes are variables inside objects**: Data an object stores

### Level 2: Understanding the Package Structure

**Explore: `ncbi_toolkit/` modules**

Each module demonstrates specific OOP principles:

#### `config.py` - Encapsulation
```python
class NCBIConfig:
    """Bundles configuration data with validation logic"""
    
    @property
    def email(self):
        """Controlled access to email attribute"""
        return self._email
    
    @email.setter
    def email(self, value):
        """Validation when setting email"""
        if "@" not in value:
            raise ValueError("Invalid email")
        self._email = value
```

**Learn**: How classes protect and validate data

#### `entrez_client.py` - Single Responsibility & Abstraction
```python
class EntrezClient:
    """Only responsible for NCBI API communication"""
    
    def search_and_fetch(self, database, term, max_results):
        """Simple interface hiding complex API calls"""
        # Complex implementation hidden here
        pass
```

**Learn**: How classes simplify complex operations

#### `record_analyzer.py` - Stateless Methods
```python
class RecordAnalyzer:
    """Groups related analysis methods together"""
    
    def calculate_gc_content(self, record):
        """Analyzes a record without storing state"""
        pass
    
    def filter_by_length(self, records, min_length):
        """Works on collections"""
        pass
```

**Learn**: How to organize related functionality

#### `record_exporter.py` - Stateful Objects
```python
class RecordExporter:
    """Maintains configuration (output directory)"""
    
    def __init__(self, output_dir):
        """Set up state when created"""
        self.output_dir = output_dir
    
    def export_fasta(self, records, filename):
        """Uses stored configuration"""
        path = self.output_dir / filename
        # export logic
```

**Learn**: How objects maintain state

### Level 3: Advanced OOP Concepts

**Study: `examples_advanced.py`**

Run advanced examples:
```bash
python examples_advanced.py
```

#### Inheritance Example
```python
class ProteinAnalyzer(RecordAnalyzer):
    """Specialized analyzer for proteins"""
    
    def calculate_molecular_weight(self, record):
        """New method - added functionality"""
        return len(record.seq) * 110
    
    def get_basic_info(self, record):
        """Overridden method - extended functionality"""
        info = super().get_basic_info(record)  # Call parent
        info['molecular_weight'] = self.calculate_molecular_weight(record)
        return info
```

**Learn**: How to extend classes with inheritance

#### Composition Example
```python
class ResearchWorkflow:
    """Coordinates multiple objects to accomplish complex tasks"""
    
    def __init__(self, config):
        self.client = EntrezClient(config)      # Has-a relationship
        self.analyzer = RecordAnalyzer()        # Has-a relationship
        self.exporter = RecordExporter()        # Has-a relationship
    
    def run_study(self):
        """Uses all three objects together"""
        records = self.client.search_and_fetch(...)
        filtered = self.analyzer.filter_by_length(records, ...)
        self.exporter.export_fasta(filtered, ...)
```

**Learn**: How objects collaborate

### Level 4: Real Workflows

**Run: `main.py`**

```bash
python main.py
```

This demonstrates a complete research workflow combining all components.

## 🎓 OOP Concepts Reference

### 1. Classes and Objects

**Class** = Blueprint/Template
**Object** = Specific instance created from the class

```python
# Class definition (blueprint)
class NCBIConfig:
    def __init__(self, email):
        self.email = email

# Object creation (instance)
config1 = NCBIConfig("alice@example.com")  # First instance
config2 = NCBIConfig("bob@example.com")    # Second instance
```

### 2. Encapsulation

Bundling data and methods that operate on that data within a class.

```python
class RecordExporter:
    def __init__(self, output_dir):
        self.output_dir = output_dir  # Data
    
    def export_fasta(self, records, filename):  # Method using that data
        path = self.output_dir / filename
        # save to path
```

**Benefits**: 
- Keeps related things together
- Controls how data is accessed
- Hides implementation details

### 3. Inheritance

Creating a new class based on an existing class.

```python
class RecordAnalyzer:              # Parent/Base class
    def get_basic_info(self):
        pass

class ProteinAnalyzer(RecordAnalyzer):  # Child/Derived class
    def calculate_molecular_weight(self):  # New method
        pass
```

**Benefits**:
- Code reuse
- Specialization
- Logical hierarchy

### 4. Composition

Objects containing other objects.

```python
class ResearchWorkflow:
    def __init__(self, config):
        self.client = EntrezClient(config)      # Contains a client
        self.analyzer = RecordAnalyzer()        # Contains an analyzer
```

**Benefits**:
- Flexibility
- Better than deep inheritance hierarchies
- "Has-a" relationships

### 5. Abstraction

Hiding complex implementation behind simple interfaces.

```python
# Complex implementation hidden
client.search_and_fetch(database="nucleotide", term="insulin", max_results=10)

# Instead of manually doing:
# 1. Configure Entrez
# 2. Open search handle
# 3. Read results
# 4. Close handle
# 5. Open fetch handle
# 6. Parse records
# 7. Close handle
```

## 🔄 Comparing Procedural vs OOP

### Original Procedural Code (`DBconnect.py`)
```python
# Global configuration
Entrez.email = "xxxx@mail.com"
Entrez.api_key = "xxxx"

# Functions scattered throughout
handle = Entrez.esearch(db="nucleotide", term='...', retmax="40")
record = Entrez.read(handle)
handle.close()

# ... more scattered code ...
```

**Issues**:
- Configuration scattered
- No reusability
- Hard to test
- Difficult to maintain

### OOP Approach (This Project)
```python
# Configuration encapsulated
config = NCBIConfig(email="xxx@mail.com", api_key="xxx")

# Functionality organized
client = EntrezClient(config)
records = client.search_and_fetch(database="nucleotide", term='...', max_results=40)

# Easy to reuse
analyzer = RecordAnalyzer()
exporter = RecordExporter()
```

**Benefits**:
- Clear organization
- Reusable components
- Easy to test
- Easy to extend

## 💡 Common OOP Patterns Used

### Dependency Injection
```python
class EntrezClient:
    def __init__(self, config: NCBIConfig):  # Config is injected
        self.config = config
```

**Why**: Makes testing easier, increases flexibility

### Factory Methods (Alternative Constructors)
```python
# Regular constructor
config = NCBIConfig(email="x@x.com")

# Alternative constructor
config = NCBIConfig.from_env()  # Reads from environment
```

**Why**: Provides multiple ways to create objects

### Property Decorators
```python
class NCBIConfig:
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email")
        self._email = value
```

**Why**: Controlled access with validation

## 🔧 Customization Examples

### Adding a New Analysis Method

Edit `ncbi_toolkit/record_analyzer.py`:

```python
def find_restriction_sites(self, record: SeqRecord, enzyme: str) -> List[int]:
    """
    Find restriction enzyme cut sites.
    
    Args:
        record: Sequence record to analyze
        enzyme: Enzyme recognition sequence
        
    Returns:
        List of positions where enzyme cuts
    """
    seq_str = str(record.seq).upper()
    enzyme = enzyme.upper()
    positions = []
    
    start = 0
    while True:
        pos = seq_str.find(enzyme, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    return positions
```

Use it:
```python
analyzer = RecordAnalyzer()
sites = analyzer.find_restriction_sites(record, "GAATTC")  # EcoRI
print(f"EcoRI sites found at positions: {sites}")
```

### Creating a Custom Exporter Format

Edit `ncbi_toolkit/record_exporter.py`:

```python
def export_markdown(self, records: List[SeqRecord], filename: str) -> Path:
    """Export records as a Markdown document."""
    output_path = self._get_output_path(filename, ".md")
    
    with open(output_path, 'w') as f:
        f.write("# Sequence Records\n\n")
        for i, record in enumerate(records, 1):
            f.write(f"## {i}. {record.id}\n\n")
            f.write(f"**Description**: {record.description}\n\n")
            f.write(f"**Length**: {len(record.seq)} bp\n\n")
            f.write(f"```\n{record.seq[:100]}...\n```\n\n")
    
    return output_path
```

## 📝 Best Practices Demonstrated

1. ✅ **Type hints**: All methods have type annotations
2. ✅ **Docstrings**: Every class and method documented
3. ✅ **Single Responsibility**: Each class has one clear purpose
4. ✅ **DRY (Don't Repeat Yourself)**: Code reuse through methods
5. ✅ **Separation of Concerns**: Different aspects in different modules
6. ✅ **Meaningful Names**: Clear, descriptive variable/method names
7. ✅ **Error Handling**: Validation and error messages
8. ✅ **Resource Management**: Proper file handling with context managers

## 🐛 Common Pitfalls to Avoid

### ❌ Don't: Modify class attributes directly
```python
exporter._output_dir = "new_path"  # Bypasses validation
```

### ✅ Do: Use public interfaces
```python
exporter = RecordExporter(output_dir="new_path")
```

### ❌ Don't: Create god objects (do everything)
```python
class NCBIEverything:
    def search(self): pass
    def analyze(self): pass
    def export(self): pass
    def visualize(self): pass
    # Too many responsibilities!
```

### ✅ Do: Separate concerns
```python
client = EntrezClient(config)   # Searches
analyzer = RecordAnalyzer()     # Analyzes
exporter = RecordExporter()     # Exports
```

## 🎯 Practice Exercises

### Exercise 1: Basic Usage
Create a script that:
1. Searches for your favorite gene
2. Filters results by length
3. Exports to FASTA and CSV

### Exercise 2: Custom Analyzer
Extend `RecordAnalyzer` to add a method that counts specific k-mers in sequences.

### Exercise 3: Inheritance
Create `RNAAnalyzer` that inherits from `RecordAnalyzer` and adds RNA-specific methods.

### Exercise 4: Complete Workflow
Create a `GeneStudy` class that:
- Takes a gene name and organism list
- Searches NCBI for all combinations
- Analyzes and compares results
- Generates a comprehensive report

## 🔗 Resources

- **BioPython Tutorial**: https://biopython.org/wiki/Documentation
- **NCBI Entrez**: https://www.ncbi.nlm.nih.gov/books/NBK25500/
- **Python OOP Tutorial**: https://docs.python.org/3/tutorial/classes.html
- **Real Python OOP**: https://realpython.com/python3-object-oriented-programming/

## 📧 Configuration

Before running examples, update the email in the scripts:

```python
config = NCBIConfig(email="YOUR_EMAIL@example.com")
```

Optionally, add an API key for faster access:
```python
config = NCBIConfig(
    email="YOUR_EMAIL@example.com",
    api_key="YOUR_API_KEY"  # Get from NCBI
)
```

Or use environment variables:
```bash
export NCBI_EMAIL="your.email@example.com"
export NCBI_API_KEY="your_api_key"
```

Then in code:
```python
config = NCBIConfig.from_env()
```

## 🎉 Next Steps

1. ✅ Run `examples_simple.py` to see basic OOP in action
2. ✅ Read through each module in `ncbi_toolkit/` with comments
3. ✅ Run `main.py` to see a complete workflow
4. ✅ Study `examples_advanced.py` for inheritance and composition
5. ✅ Modify the code to add your own features
6. ✅ Build your own research workflow!

---

**Happy Learning! 🚀**

Remember: The best way to learn OOP is by doing. Start small, experiment, break things, and build up your understanding gradually!
