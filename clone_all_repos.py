import json
import os
import warnings
from typing import List, Tuple


def extract_repo_data_from_json(
    json_file_name: str, json_folder_path: str
) -> Tuple[List[str], List[str]]:
    # Combine json_file_name and json_folder_path to get relative path of json file
    json_file_path = os.path.join(json_folder_path, json_file_name)

    # Load the JSON data from the file
    with open(json_file_path) as f:
        data = json.load(f)

    # Extract the html_url values from the JSON data
    html_urls = [item["repo"]["html_url"] for item in data]

    # Extract the repo name from the JSON file
    repo_names = [item["repo"]["name"] for item in data]

    return html_urls, repo_names


def extract_all_html_urls(json_folder_path: str) -> Tuple[List[str], List[str]]:
    all_html_urls = []
    all_repo_names = []
    for json_file_name in os.listdir(json_folder_path):
        if not json_file_name.endswith(".json"):
            warnings.warn(f"Skipping non-JSON file: {json_file_name}")
            continue
        html_urls, repo_names = extract_repo_data_from_json(
            json_file_name, json_folder_path
        )
        all_html_urls.extend(html_urls)
        all_repo_names.extend(repo_names)
    return all_html_urls, all_repo_names


def clone_all_repos(all_html_urls: list, all_repo_names: list, target_dir: str) -> None:
    # Iterate over all html_urls and all_repo_names and clone the repo into the target_dir
    for html_url, repo_name in zip(all_html_urls, all_repo_names):
        cloned_repo_path = os.path.join(target_dir, repo_name)
        os.system(f"git clone {html_url} {cloned_repo_path}")


def main():
    json_folder_path = "all_starred_repos/ghstars-butterlyn"
    target_dir = "all_starred_repos/starred_repos"
    all_html_urls, all_repo_names = extract_all_html_urls(json_folder_path)
    clone_all_repos(all_html_urls, all_repo_names, target_dir)


if __name__ == "__main__":
    main()
