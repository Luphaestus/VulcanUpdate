import xml.etree.ElementTree as ET
import requests

repositories = {
    "Zygisk - LSPosed": ("LSPosed/LSPosed", 1),
    "Sharp++ Camera Module (N20U)": ("Luphaestus/VulcanUpdate", 0),
    "ViPER4Android Reverse Engineered": ("AndroidAudioMods/ViPER4Android", 1),
    "YouTube ReVanced eXtended": ("NoName-exe/revanced-extended", 2),
    "YouTube Music ReVanced": ("NoName-exe/revanced-extended", 1)  
}

def get_latest_download_url(repo, asset_index):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        release_data = response.json()
        if len(release_data['assets']) > asset_index:
            return release_data['assets'][asset_index]['browser_download_url']
        else:
            print(f"Asset index {asset_index} out of range for {repo}.")
    else:
        print(f"Failed to fetch releases for {repo}: {response.status_code}")
    return None

xml_file_path = './Manifests/Modules.xml'
tree = ET.parse(xml_file_path)
root = tree.getroot()

for module in root:
    package_name = module.find('package').text
    if package_name in repositories:
        repo, asset_index = repositories[package_name]
        latest_url = get_latest_download_url(repo, asset_index)
        if latest_url:
            download_url = module.find('downloadurl')
            if download_url is not None:
                print(latest_url)
                download_url.text = latest_url

tree.write(xml_file_path, encoding='UTF-8', xml_declaration=True)

print("Download URLs updated successfully.")
