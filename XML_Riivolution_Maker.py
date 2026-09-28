import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

first_query = True
mod_paths_list = []

print("================================")
print("Riivolution XML Maker v0.2")
print("================================")

while True:
    game_path = input("Please enter the path to your original Wii game directory: ")

    if game_path.strip() == "":
        print("Error: Please enter a valid path.")
        continue

    if not os.path.exists(game_path):
        print("Error: The specified path does not exist.")
        continue

    mod_path = input("Thanks now enter the path to your modded directory: ")

    if mod_path.strip() == "":
        print("Error: Please enter a valid path.")
        continue

    if not os.path.exists(mod_path):
        print("Error: The specified path does not exist.")
        continue

    mod_paths_list.append(mod_path)

    print("Thanks have you more moddes to add? (y/n): ")
    more_mods = input()
    if more_mods.lower() != "y":
        break

while True:
    if first_query:
        print("Thanks now which game version are you using? (PAL/NTSC-U/NTSC-J): ")
        first_query = False
    else:
        print("Please enter a valid game version (PAL/NTSC-U/NTSC-J): ")
    game_version = input()
    if game_version.lower() == "pal":
        with open("game_versions/SMG_PAL.txt", "r", encoding="utf-8") as pal_file:
            file_contents = pal_file.read()
        break
    elif game_version.lower() == "ntsc-u":
        with open("game_versions/SMG_NTSC-U.txt", "r", encoding="utf-8") as ntsc_u_file:
            file_contents = ntsc_u_file.read()
        break
    elif game_version.lower() == "ntsc-j":
        with open("game_versions/SMG_NTSC-J.txt", "r", encoding="utf-8") as ntsc_j_file:
            file_contents = ntsc_j_file.read()
        break
    else:
        print(
            "Invalid game version. Please enter PAL, NTSC-U, or NTSC-J. (!!!IN THIS VERSION IT ONLY WORKS FOR SMG1!!!)"
        )

while True:
    print(
        "Thanks now have you Custom Code? y/n (WARNING THIS IS AN IDEA AND NOT IMPLEMENTED YET): "
    )
    custom_code = input().strip().lower()
    if custom_code == "y":
        print("!!!THIS IS AN IDEA AND NOT IMPLEMENTED YET!!!")
        break
    elif custom_code == "n":
        break
    else:
        print("Invalid input! Please type 'y' or 'n'.\n")

while True:
    print("Thanks now which name do you want?")
    name = input()
    print("The name you entered is: " + name + " . Is this correct? (y/n): ")
    correct = input().strip().lower()
    if correct == "y":
        break
    elif correct == "n":
        continue
    else:
        print("Invalid input! Please type 'y' or 'n'.\n")

print("Thanks now we will generate the XML file for you please wait...")

first_path = mod_paths_list[0]
parent_dir = os.path.dirname(first_path.rstrip(r"\/"))
folder_root_name = os.path.basename(parent_dir)
root = ET.Element("wiidisc", version="1", root=f"/{folder_root_name}")

ET.SubElement(root, "id", game="RMG")

options = ET.SubElement(root, "options")
section = ET.SubElement(options, "section", name=name)
option = ET.SubElement(section, "option", name="Select Your Region:")

region_name = game_version.upper()
choice = ET.SubElement(option, "choice", name=region_name)

patch_id = "SMG_MOD_PATCH"
ET.SubElement(choice, "patch", id=patch_id)

patch_block = ET.SubElement(root, "patch", id=patch_id)

for path in mod_paths_list:
    folder_name = os.path.basename(path.rstrip(r"\/"))
    ET.SubElement(
        patch_block,
        "folder",
        disc=f"/{folder_name}",
        external=f"/{folder_name}",
        create="true",
    )

xml_string = ET.tostring(root, encoding="utf-8")
parsed_xml = minidom.parseString(xml_string)
pretty_xml = parsed_xml.toprettyxml(indent="  ")

output_filename = f"{name.replace(' ', '_')}.xml"
with open(output_filename, "w", encoding="utf-8") as xml_file:
    xml_file.write(pretty_xml)

print(f"\n================================================================")
print(f"Success! Your XML '{output_filename}' has been generated!")
print(f"================================================================")
