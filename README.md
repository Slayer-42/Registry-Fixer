## Windows Registry User Profile Path Replacement Tool

**Overview:**  
This tool provides a safe and interactive Python script to search, review, and batch-update Windows registry entries that reference a user profile folder path (such as after manually renaming a Windows user folder). It is especially helpful for advanced Windows users and system administrators who have changed their user profile directory and need to realign legacy configuration paths across the registry.

**Features:**

- **Searches the entire registry** for `REG_SZ` and `REG_EXPAND_SZ` values containing an old user folder path.
- For every matching entry, you can choose to:
  - Replace the old path with a new one
  - Delete the registry value
  - Skip the entry
  - Replace all remaining entries automatically (*replace all* option)
- **Collision/conflict handling:** If a replace fails (e.g., due to a name conflict or permissions), you are prompted to delete or skip that specific entry.
- **Color-coded console output** via colorama for maximum clarity (success in green, deletes in red, skips in yellow, errors in red).
- **No changes made without confirmation:** User-driven step-by-step or bulk processing ensures maximum control and safety.
- **Supports both** HKEY_CURRENT_USER and HKEY_LOCAL_MACHINE hives.

**Use Cases:**

- You’ve renamed your Windows user profile folder and want to update all registry references from the old path to the new path.
- You need to batch-clean deprecated or incorrect profile folder references left over from Windows upgrades or user migrations.
- Useful for fixing application install/uninstall issues, path-related configuration errors, or corruption after a user folder rename.

**Requirements:**

- **Python 3** (tested on 3.6+)
- **colorama** library (`pip install colorama`)
- Administrative permissions required to access and modify most registry keys.

**Important Notes:**

- Direct user profile renaming is not supported by Microsoft. This tool is intended as a recovery/automation aid for knowledgeable users.
- Always **back up your Windows registry** before making changes.
- Test first in a controlled environment or virtual machine when possible.

**Contribution:**

Contributions, bug reports, and feature suggestions are welcome! Please open an issue or submit a pull request on this repository.