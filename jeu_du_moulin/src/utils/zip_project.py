import zipfile
import os

def create_zip(directory, output_filename):
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, directory)
                zipf.write(filepath, arcname)

if __name__ == "__main__":
    create_zip(r"c:\Users\HP\Desktop\nv jeux\jeu_du_moulin", "jeu_du_moulin.zip")
    print("Project zipped successfully!")