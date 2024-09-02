from PIL import Image

# Carica l'immagine
image = Image.open('./public/assets/Attack_1.png')

# Dimensioni del frame
frame_width = 70
frame_height = 64

# Numero di frame da estrarre
num_frames = 5

# Dividere l'immagine in frame
for i in range(num_frames):
    # Calcolare la posizione x per ogni frame
    left = i * frame_width
    upper = 0
    right = left + frame_width
    lower = upper + frame_height
    
    # Ritagliare il frame dall'immagine originale
    frame = image.crop((left, upper, right, lower))
    
    # Salva il frame come nuova immagine
    frame.save(f'attack_1_{i}.png')

print("Suddivisione completata!")
