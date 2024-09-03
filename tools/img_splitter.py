import os
from PIL import Image
import glob

# Percorso della cartella contenente i file di input
input_folder = './public/assets/new_animations/enemy/'

# Dimensioni del frame
frame_width = 128
frame_height = 128

# Trova tutti i file .png nella cartella di input
files = glob.glob(os.path.join(input_folder, '*.png'))

for file in files:
    # Carica l'immagine
    image = Image.open(file)
    
    # Estrai il nome del file senza estensione e converti in minuscolo
    filename = os.path.basename(file).split('.')[0].lower()
    
    # Crea una cartella per salvare i frame
    output_folder = os.path.join(input_folder, filename)
    os.makedirs(output_folder, exist_ok=True)
    
    # Calcola il numero di frame in base alla larghezza dell'immagine
    img_width, img_height = image.size
    num_frames = img_width // frame_width
    
    # Dividi l'immagine in frame
    for i in range(num_frames):
        # Calcola la posizione x per ogni frame
        left = i * frame_width
        upper = 0
        right = left + frame_width
        lower = upper + frame_height
        
        # Ritaglia il frame dall'immagine originale
        frame = image.crop((left, upper, right, lower))
        
        # Salva il frame nella cartella corrispondente
        frame.save(os.path.join(output_folder, f'{i}_.png'))

print("Suddivisione completata!")
