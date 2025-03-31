#!/usr/bin/env python3
import json
import os
import re
import shutil


def get_valid_filename(prompt, default):
    """
    Prompt the user for a file name that can contain only letters, numbers, and underscores.
    Spaces are automatically replaced with underscores.
    """
    while True:
        inp = input(prompt).strip()
        if not inp:
            inp = default
        # Validate: only letters, numbers, and underscores allowed.
        if re.fullmatch(r"[A-Za-z0-9_]+", inp):
            return inp
        else:
            print(
                "Invalid input. Please use only letters, numbers, and underscores."
            )


def create_new_config():
    """
    Interactively ask for main menu items and sub menu items.
    Returns a list of dictionaries representing the configuration.
    """
    print("Creating a new configuration file.")
    raw_main_menu_input = input(
        "Enter main menu items separated by commas (e.g. Account, Reports, Tools): "
    )
    raw_main_menus = [
        x.strip() for x in raw_main_menu_input.split(",") if x.strip()
    ]
    config_data = []
    for raw_menu in raw_main_menus:
        entry = {}
        entry["display"] = raw_menu  # preserve original display text
        entry["folder"] = raw_menu.lower().replace(" ", "_")
        sub_input = input(
            f"Enter sub menu items for '{raw_menu}' separated by commas (or leave blank if none): "
        )
        if sub_input.strip():
            raw_subs = [x.strip() for x in sub_input.split(",") if x.strip()]
            pages = []
            for raw_sub in raw_subs:
                page = {}
                page["display"] = raw_sub
                default_filename = raw_sub.lower().replace(" ", "_")
                valid_filename = get_valid_filename(
                    f"  Enter file name for '{raw_sub}' (only letters, numbers, and underscores allowed, default: {default_filename}): ",
                    default_filename,
                )
                page["file_path"] = f"{entry['folder']}/{valid_filename}.py"
                icon = input(
                    f"  Enter icon for '{raw_sub}' (default: empty): "
                ).strip()
                page["icon"] = icon
                pages.append(page)
            entry["pages"] = pages
        else:
            # Standalone main menu item.
            page = {}
            default_filename = entry["folder"]
            valid_filename = get_valid_filename(
                f"Enter file name for main menu item '{raw_menu}' (only letters, numbers, and underscores allowed, default: {default_filename}): ",
                default_filename,
            )
            page["file_path"] = f"{entry['folder']}/{valid_filename}.py"
            icon = input(
                f"Enter icon for main menu item '{raw_menu}' (default: empty): "
            ).strip()
            page["icon"] = icon
            entry["page"] = page
        config_data.append(entry)
    return config_data


def load_config():
    """
    Ask the user for a config file path (default: menu_config.json) and load the JSON.
    """
    config_path = (
        input("Enter config file path (default: menu_config.json): ").strip()
        or "menu_config.json"
    )
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config_data = json.load(f)
        print(f"Configuration loaded from {config_path}.")
        return config_data
    else:
        print(
            f"File {config_path} does not exist. Creating a new configuration."
        )
        return create_new_config()


def modify_config(config_data):
    """
    Ask the user if they want to add or remove any main menu or sub menu items.
    Update the configuration (and file system) accordingly.
    """
    while True:
        print("\nCurrent configuration:")
        for idx, entry in enumerate(config_data, start=1):
            print(f" {idx}. {entry['display']}")
            if "pages" in entry:
                for jdx, page in enumerate(entry["pages"], start=1):
                    print(f"     {jdx}. {page['display']}")
        choice = (
            input(
                "\nWould you like to modify the configuration? (add/remove/none): "
            )
            .strip()
            .lower()
        )
        if choice in ["none", "n"]:
            break
        elif choice == "add":
            add_choice = (
                input("Add a main menu item or a sub menu item? (main/sub): ")
                .strip()
                .lower()
            )
            if add_choice == "main":
                # Add a new main menu item.
                new_menu = input("Enter the new main menu item name: ").strip()
                if not new_menu:
                    print("No name entered. Skipping.")
                    continue
                new_entry = {}
                new_entry["display"] = new_menu
                new_entry["folder"] = new_menu.lower().replace(" ", "_")
                sub = (
                    input(f"Does '{new_menu}' have sub menu items? (y/n): ")
                    .strip()
                    .lower()
                )
                if sub == "y":
                    raw_subs = input(
                        f"Enter sub menu items for '{new_menu}' separated by commas: "
                    ).split(",")
                    pages = []
                    for raw_sub in raw_subs:
                        raw_sub = raw_sub.strip()
                        if not raw_sub:
                            continue
                        page = {}
                        page["display"] = raw_sub
                        default_filename = raw_sub.lower().replace(" ", "_")
                        valid_filename = get_valid_filename(
                            f"  Enter file name for '{raw_sub}' (default: {default_filename}): ",
                            default_filename,
                        )
                        page["file_path"] = (
                            f"{new_entry['folder']}/{valid_filename}.py"
                        )
                        icon = input(
                            f"  Enter icon for '{raw_sub}' (default: empty): "
                        ).strip()
                        page["icon"] = icon
                        pages.append(page)
                    new_entry["pages"] = pages
                else:
                    page = {}
                    default_filename = new_entry["folder"]
                    valid_filename = get_valid_filename(
                        f"Enter file name for main menu item '{new_menu}' (default: {default_filename}): ",
                        default_filename,
                    )
                    page["file_path"] = (
                        f"{new_entry['folder']}/{valid_filename}.py"
                    )
                    icon = input(
                        f"Enter icon for main menu item '{new_menu}' (default: empty): "
                    ).strip()
                    page["icon"] = icon
                    new_entry["page"] = page
                config_data.append(new_entry)
                os.makedirs(new_entry["folder"], exist_ok=True)
                if "pages" in new_entry:
                    for page in new_entry["pages"]:
                        if not os.path.exists(page["file_path"]):
                            with open(page["file_path"], "w") as fp:
                                fp.write(
                                    "# Empty script for "
                                    + page["display"]
                                    + "\n"
                                )
                            print(f"Created file: {page['file_path']}")
                else:
                    page = new_entry["page"]
                    if not os.path.exists(page["file_path"]):
                        with open(page["file_path"], "w") as fp:
                            fp.write(
                                "# Empty script for "
                                + new_entry["display"]
                                + "\n"
                            )
                        print(f"Created file: {page['file_path']}")
                print(f"Added new main menu item '{new_menu}'.")
            elif add_choice == "sub":
                # Add a new sub menu item to an existing main menu.
                target = input(
                    "Enter the main menu item (display name) to add a sub menu item to: "
                ).strip()
                found = None
                for entry in config_data:
                    if entry["display"].lower() == target.lower():
                        found = entry
                        break
                if not found:
                    print(f"No main menu item named '{target}' found.")
                    continue
                # If this main menu is currently standalone, ask if we should convert it.
                if "page" in found:
                    conv = (
                        input(
                            f"'{found['display']}' is currently standalone. Convert to a menu with sub menu items? (y/n): "
                        )
                        .strip()
                        .lower()
                    )
                    if conv == "y":
                        existing_page = found.pop("page")
                        found["pages"] = [
                            {
                                "display": found["display"],
                                "file_path": existing_page["file_path"],
                                "icon": existing_page.get("icon", ""),
                            }
                        ]
                    else:
                        print("Skipping addition.")
                        continue
                # Now add a new sub menu item.
                new_sub = input("Enter the new sub menu item name: ").strip()
                if not new_sub:
                    print("No name entered. Skipping.")
                    continue
                page = {}
                page["display"] = new_sub
                default_filename = new_sub.lower().replace(" ", "_")
                valid_filename = get_valid_filename(
                    f"  Enter file name for '{new_sub}' (default: {default_filename}): ",
                    default_filename,
                )
                page["file_path"] = f"{found['folder']}/{valid_filename}.py"
                icon = input(
                    f"  Enter icon for '{new_sub}' (default: empty): "
                ).strip()
                page["icon"] = icon
                found["pages"].append(page)
                # Ensure the main menu folder exists before writing the file.
                os.makedirs(found["folder"], exist_ok=True)
                if not os.path.exists(page["file_path"]):
                    with open(page["file_path"], "w") as fp:
                        fp.write("# Empty script for " + new_sub + "\n")
                    print(f"Created file: {page['file_path']}")
                print(
                    f"Added sub menu item '{new_sub}' to '{found['display']}'."
                )
            else:
                print("Invalid add option. Please enter 'main' or 'sub'.")
        elif choice == "remove":
            rem_choice = (
                input(
                    "Remove a main menu item or a sub menu item? (main/sub): "
                )
                .strip()
                .lower()
            )
            if rem_choice == "main":
                target = input(
                    "Enter the main menu item (display name) to remove: "
                ).strip()
                idx_to_remove = None
                for idx, entry in enumerate(config_data):
                    if entry["display"].lower() == target.lower():
                        idx_to_remove = idx
                        break
                if idx_to_remove is not None:
                    confirm = (
                        input(
                            f"Are you sure you want to remove main menu item '{config_data[idx_to_remove]['display']}' and its folder? (y/n): "
                        )
                        .strip()
                        .lower()
                    )
                    if confirm == "y":
                        folder = config_data[idx_to_remove]["folder"]
                        if os.path.exists(folder):
                            shutil.rmtree(folder)
                            print(f"Removed folder '{folder}'.")
                        removed_item = config_data.pop(idx_to_remove)
                        print(
                            f"Removed main menu item '{removed_item['display']}'."
                        )
                    else:
                        print("Removal canceled.")
                else:
                    print(f"Main menu item '{target}' not found.")
            elif rem_choice == "sub":
                target = input(
                    "Enter the main menu item (display name) that contains the sub menu item: "
                ).strip()
                found = None
                for entry in config_data:
                    if entry["display"].lower() == target.lower():
                        found = entry
                        break
                if not found:
                    print(f"No main menu item named '{target}' found.")
                    continue
                if "pages" not in found:
                    print(
                        f"'{found['display']}' does not have sub menu items."
                    )
                    continue
                print("Sub menu items:")
                for idx, page in enumerate(found["pages"], start=1):
                    print(f" {idx}. {page['display']}")
                sub_target = input(
                    "Enter the sub menu item (display name) to remove: "
                ).strip()
                idx_to_remove = None
                for idx, page in enumerate(found["pages"]):
                    if page["display"].lower() == sub_target.lower():
                        idx_to_remove = idx
                        break
                if idx_to_remove is not None:
                    confirm = (
                        input(
                            f"Are you sure you want to remove sub menu item '{found['pages'][idx_to_remove]['display']}'? (y/n): "
                        )
                        .strip()
                        .lower()
                    )
                    if confirm == "y":
                        file_path = found["pages"][idx_to_remove]["file_path"]
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"Removed file '{file_path}'.")
                        removed_page = found["pages"].pop(idx_to_remove)
                        print(
                            f"Removed sub menu item '{removed_page['display']}'."
                        )
                    else:
                        print("Removal canceled.")
                else:
                    print(f"Sub menu item '{sub_target}' not found.")
            else:
                print("Invalid remove option. Please enter 'main' or 'sub'.")
        else:
            print("Invalid choice. Please enter add, remove, or none.")
    return config_data


def generate_app_code(config_data):
    """
    Generate a Streamlit app that loads the JSON configuration (from menu_config.json)
    and uses st.navigation to build a sidebar with categories and sub menu items.
    This version does not include login or logout functionality.
    """
    lines = []
    lines.append("import json")
    lines.append("import os")
    lines.append("import streamlit as st")
    lines.append("")
    lines.append("# Load the menu configuration from the JSON file")
    lines.append("with open('menu_config.json', 'r') as f:")
    lines.append("    menu_config = json.load(f)")
    lines.append("")
    lines.append("# Dynamically create st.Page definitions")
    lines.append("pages = {}")
    lines.append("for menu in menu_config:")
    lines.append("    if 'pages' in menu:")
    lines.append("        for page in menu['pages']:")
    lines.append(
        "            var_name = page['display'].lower().replace(' ', '_')"
    )
    lines.append("            if page.get('icon'):")
    lines.append(
        "                pages[var_name] = st.Page(page['file_path'], title=page['display'], icon=page['icon'])"
    )
    lines.append("            else:")
    lines.append(
        "                pages[var_name] = st.Page(page['file_path'], title=page['display'])"
    )
    lines.append("    else:")
    lines.append("        var_name = menu['folder']")
    lines.append("        page = menu['page']")
    lines.append("        if page.get('icon'):")
    lines.append(
        "            pages[var_name] = st.Page(page['file_path'], title=menu['display'], icon=page['icon'])"
    )
    lines.append("        else:")
    lines.append(
        "            pages[var_name] = st.Page(page['file_path'], title=menu['display'])"
    )
    lines.append("")
    lines.append("# Build navigation sidebar")
    lines.append("with st.sidebar:")
    lines.append("    st.header('Navigation')")
    lines.append(
        "    category = st.selectbox('Select a category', [m['display'] for m in menu_config])"
    )
    lines.append(
        "    current_menu = next((m for m in menu_config if m['display'] == category), None)"
    )
    lines.append("    if current_menu:")
    lines.append("        if 'pages' in current_menu:")
    lines.append(
        "            option = st.selectbox('Select an option', [p['display'] for p in current_menu['pages']])"
    )
    lines.append("            var_name = option.lower().replace(' ', '_')")
    lines.append("            current_page = pages[var_name]")
    lines.append("        else:")
    lines.append("            var_name = current_menu['folder']")
    lines.append("            current_page = pages[var_name]")
    lines.append("")
    lines.append("pg = st.navigation([current_page])")
    lines.append("pg.run()")

    output_file = "generated_app.py"
    with open(output_file, "w") as f:
        f.write("\n".join(lines))
    print(f"Streamlit app generated as '{output_file}'.")


def create_folders_and_files(config_data):
    """
    Create folders for each main menu item and empty Python scripts for each page if they do not exist.
    """
    for entry in config_data:
        folder = entry["folder"]
        os.makedirs(folder, exist_ok=True)
        if "pages" in entry:
            for page in entry["pages"]:
                if not os.path.exists(page["file_path"]):
                    with open(page["file_path"], "w") as fp:
                        fp.write(
                            "# Empty script for " + page["display"] + "\n"
                        )
                    print(f"Created file: {page['file_path']}")
        else:
            page = entry["page"]
            if not os.path.exists(page["file_path"]):
                with open(page["file_path"], "w") as fp:
                    fp.write("# Empty script for " + entry["display"] + "\n")
                print(f"Created file: {page['file_path']}")
    print("Folders and files have been created.")


def main():
    load_choice = (
        input("Would you like to load an existing configuration file? (y/n): ")
        .strip()
        .lower()
    )
    if load_choice == "y":
        config_data = load_config()
    else:
        config_data = create_new_config()

    mod_choice = (
        input(
            "Would you like to modify the configuration (add/remove items)? (y/n): "
        )
        .strip()
        .lower()
    )
    if mod_choice == "y":
        config_data = modify_config(config_data)

    config_file = "menu_config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=4)
    print(f"Configuration saved to '{config_file}'.")

    generate_app_code(config_data)
    create_folders_and_files(config_data)
    print("\nAll done! To run your Streamlit app, use:")
    print("   streamlit run generated_app.py")


if __name__ == "__main__":
    main()
