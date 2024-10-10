#Modrinth Modpack Downloader
import json
import os
import zipfile
import urllib.request
import threading
import asyncio
import time

current_time = time.time()
dir = os.getcwd()

def download_mod(mod_index, folder_name):
	mod_name = mod_index["path"].split("/")[1]
	urllib.request.urlretrieve(mod_index["downloads"][0], dir+"/"+folder_name+"/"+mod_name)
	print(mod_name, "был скачан")

def get_modpack_index():
	for file in os.listdir():
		if file.endswith(".mrpack"):
			with zipfile.ZipFile(dir + "/" + file, 'r') as modpack:
				with modpack.open("modrinth.index.json") as index:
					content = index.read()
					return json.loads(content.decode('utf-8'))

def main():
	modpack_index = get_modpack_index()
	folder_name = f'{modpack_index["name"]} {modpack_index["versionId"]}'
	threads = []
	os.makedirs(folder_name, exist_ok=True)
	for mod_index in modpack_index["files"]:
		thread = threading.Thread(target=download_mod, args=(mod_index, folder_name))
		thread.start()
		threads.append(thread)
	
	for thread in threads:
		thread.join()

	print(f'\nМоды скачаны в папку: "{dir+"/"+folder_name}"')

if __name__ == "__main__":
	main()