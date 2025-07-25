import winreg
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

old_path = r'C:\Users\Your Old Profile Name'
new_path = r'C:\Users\Your New Profile Name'

found_entries = []

def search_registry_for_old_path(root, path):
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as key:
            i = 0
            while True:
                try:
                    value = winreg.EnumValue(key, i)
                    name, data, data_type = value
                    if data_type in (winreg.REG_SZ, winreg.REG_EXPAND_SZ) and old_path in data:
                        full_key_path = f"{root_to_str(root)}\\{path}" if path else root_to_str(root)
                        found_entries.append((full_key_path, name, data_type, data))
                    i += 1
                except OSError:
                    break
    except Exception:
        # Access Denied or key doesn't exist, skip silently
        pass

    # Recursively search subkeys
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as key:
            i = 0
            while True:
                try:
                    subkey = winreg.EnumKey(key, i)
                    new_path_to_search = path + "\\" + subkey if path else subkey
                    search_registry_for_old_path(root, new_path_to_search)
                    i += 1
                except OSError:
                    break
    except Exception:
        pass

def process_registry_entries():
    updated_count = 0
    deleted_count = 0
    skipped_count = 0
    replace_all_mode = False  # Flag to replace all remaining without asking

    for full_key_path, name, data_type, data in found_entries:
        root_name, sub_path = split_root_from_key(full_key_path)
        root = str_to_root(root_name)
        if root is None:
            print(f"Unknown root hive: {root_name}. Skipping {full_key_path}\\{name}")
            skipped_count += 1
            continue

        print("\n---------------------------------------------")
        print(f"Key: {full_key_path}")
        print(f"Value Name: {name}")
        print(f"Current Data: {data}")

        if not replace_all_mode:
            print("Options: [r]eplace, [d]elete, [s]kip, [a] replace ALL remaining entries automatically")
            while True:
                choice = input("Enter your choice (r/d/s/a): ").strip().lower()
                if choice in ('r', 'd', 's', 'a'):
                    break
                else:
                    print("Invalid input. Please enter 'r', 'd', 's', or 'a'.")
            if choice == 'a':
                replace_all_mode = True
                choice = 'r'  # Proceed replacing this current too
        else:
            choice = 'r'  # Automatically replace when in replace all mode

        try:
            with winreg.OpenKey(root, sub_path, 0, winreg.KEY_SET_VALUE) as key:
                if choice == 'r':
                    new_data = data.replace(old_path, new_path)
                    winreg.SetValueEx(key, name, 0, data_type, new_data)
                    print(f"{Fore.GREEN}Replaced old path with new path in {full_key_path}\\{name}{Style.RESET_ALL}")
                    updated_count += 1
                elif choice == 'd':
                    winreg.DeleteValue(key, name)
                    print(f"{Fore.RED}Deleted the registry value {full_key_path}\\{name}{Style.RESET_ALL}")
                    deleted_count += 1
                elif choice == 's':
                    print(f"{Fore.YELLOW}Skipped {full_key_path}\\{name}{Style.RESET_ALL}")
                    skipped_count += 1
        except Exception as e:
            if choice == 'r':
                print(f"{Fore.RED}Failed to replace {full_key_path}\\{name}: {e}{Style.RESET_ALL}")
            elif choice == 'd':
                print(f"{Fore.RED}Failed to delete {full_key_path}\\{name}: {e}{Style.RESET_ALL}")
            elif choice == 's':
                print(f"{Fore.RED}Failed to skip {full_key_path}\\{name}: {e}{Style.RESET_ALL}")

    print("\n---------------------------------------------")
    print(f"Operation completed. {Fore.GREEN}{updated_count} entries replaced{Style.RESET_ALL}, "\
          f"{Fore.RED}{deleted_count} entries deleted{Style.RESET_ALL}, "\
          f"{Fore.YELLOW}{skipped_count} entries skipped{Style.RESET_ALL}.")

def root_to_str(root):
    if root == winreg.HKEY_CURRENT_USER:
        return "HKEY_CURRENT_USER"
    elif root == winreg.HKEY_LOCAL_MACHINE:
        return "HKEY_LOCAL_MACHINE"
    elif root == winreg.HKEY_CLASSES_ROOT:
        return "HKEY_CLASSES_ROOT"
    elif root == winreg.HKEY_USERS:
        return "HKEY_USERS"
    elif root == winreg.HKEY_CURRENT_CONFIG:
        return "HKEY_CURRENT_CONFIG"
    else:
        return str(root)

def str_to_root(name):
    mapping = {
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKEY_USERS": winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
    }
    return mapping.get(name)

def split_root_from_key(full_key_path):
    parts = full_key_path.split("\\", 1)
    root = parts[0]
    sub_path = parts[1] if len(parts) > 1 else ""
    return root, sub_path

if __name__ == "__main__":
    print(f"Searching registry for entries containing '{old_path}'...\n(This may take some time)")

    roots_to_search = [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_USERS]
    for root in roots_to_search:
        search_registry_for_old_path(root, "")

    if not found_entries:
        print("No registry entries found containing the old path.")
    else:
        print(f"\nFound {len(found_entries)} entries containing the old path.")
        process_registry_entries()