# MarkAI Import Solutions Guide

## 🚨 Common Import Problems & Solutions

### Problem 1: "ModuleNotFoundError: No module named 'core'"
**Cause**: Python can't find your project modules because the project root isn't in Python path.

**Solution**: Use the import helper at the top of your scripts:
```python
from utils.import_helper import setup_project_imports
setup_project_imports()

# Now all imports work
from core.ai_engine import MarkAICore
from memory.conversation_manager import ConversationManager
```

### Problem 2: "ImportError: attempted relative import with no known parent package"
**Cause**: Using relative imports incorrectly or outside a package context.

**Solution**: Use absolute imports instead:
```python
# ❌ Don't do this
from .ai_engine import MarkAICore

# ✅ Do this
from core.ai_engine import MarkAICore
```

### Problem 3: Import works in one file but not another
**Cause**: Inconsistent Python path setup across files.

**Solution**: Use the import helper consistently in all entry points:
```python
# Add this to the top of EVERY main script
from utils.import_helper import setup_project_imports
setup_project_imports()
```

## 🛠️ Complete Setup Instructions

### Step 1: Use Import Helper (Recommended)
Add this to the top of any script that imports MarkAI modules:

```python
#!/usr/bin/env python3
"""Your script"""

# Setup imports first, before any MarkAI imports
from utils.import_helper import setup_project_imports
setup_project_imports()

# Now import MarkAI modules
from core.ai_engine import MarkAICore
from utils.config import Config
```

### Step 2: Alternative - Manual Setup
If you can't use the import helper:

```python
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent  # Adjust as needed
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Now imports work
from core.ai_engine import MarkAICore
```

### Step 3: Production Environment
Set the PYTHONPATH environment variable:

**Windows:**
```cmd
set PYTHONPATH=D:\files\coding\genAi\MarkAi;%PYTHONPATH%
```

**Linux/Mac:**
```bash
export PYTHONPATH=/path/to/MarkAi:$PYTHONPATH
```

## 📁 Project Structure Requirements

Ensure your project has this structure with `__init__.py` files:

```
MarkAi/
├── __init__.py           # Makes MarkAi a package
├── main.py              # Entry point
├── core/
│   ├── __init__.py      # Makes core a package
│   └── ai_engine.py
├── memory/
│   ├── __init__.py
│   ├── conversation_manager.py
│   └── context_manager.py
├── plugins/
│   ├── __init__.py
│   └── plugin_manager.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   └── import_helper.py
├── cli/
│   ├── __init__.py
│   └── interface.py
└── api/
    ├── __init__.py
    └── server.py
```

## 🧪 Testing Your Imports

Run the import test script to verify everything works:

```bash
cd /path/to/MarkAi
python test_imports.py
```

This will show you:
- ✅ Which modules import successfully
- ❌ Which modules have problems
- 📁 Your current project structure
- 🐍 Your Python path configuration

## 🔧 Troubleshooting Commands

### Debug Current Setup
```python
from utils.import_helper import debug_imports
debug_imports()
```

### Check Python Path
```python
import sys
print("Python path:")
for i, path in enumerate(sys.path):
    print(f"  {i+1}. {path}")
```

### Test Specific Module
```python
try:
    from core.ai_engine import MarkAICore
    print("✅ Import successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
```

## 🎯 Best Practices

1. **Always use the import helper** for MarkAI projects
2. **Use absolute imports** (not relative)
3. **Add import setup at the top** of main scripts
4. **Keep `__init__.py` files** in all package directories
5. **Test imports regularly** using the test script
6. **Set PYTHONPATH in production** environments

## 🚀 Quick Fix Checklist

If imports are broken:

- [ ] Run `python utils/import_helper.py` to diagnose
- [ ] Add `from utils.import_helper import setup_project_imports; setup_project_imports()` to your script
- [ ] Check that `__init__.py` files exist in all directories
- [ ] Use absolute imports (not relative)
- [ ] Run `python test_imports.py` to verify fix

## 📞 Common Scenarios

### Scenario 1: New script in project root
```python
from utils.import_helper import setup_project_imports
setup_project_imports()

from core.ai_engine import MarkAICore
# ... rest of your code
```

### Scenario 2: Script in subdirectory
```python
# If your script is in subdirectory, adjust the path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.import_helper import setup_project_imports
setup_project_imports()
```

### Scenario 3: External script importing MarkAI
```python
import sys
sys.path.insert(0, "/path/to/MarkAi")

from utils.import_helper import setup_project_imports
setup_project_imports()

from core.ai_engine import MarkAICore
```

This guide should solve 99% of Python import issues in the MarkAI project! 🎉
