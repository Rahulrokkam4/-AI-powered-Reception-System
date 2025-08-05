import os
import cv2
import faiss
import pickle
import numpy as np
from face_analyzer import app



class FaceRecognition:
    def __init__(self):
        self.face_embedding = []
        self.face_label = []
        self.index_path = "embeddings/index.faiss"
        self.label_path = "embeddings/label.pkl"
        os.makedirs("embeddings", exist_ok=True)
    # register image into database & faiss index 
    def register_face(self, image_path, name):
        # Read image
        img = cv2.imread(image_path)
        faces = app.get(img)

        if not faces:
            print("No face detected.")
            return

        face = faces[0]
        emb = face.embedding.astype("float32")
        emb /= np.linalg.norm(emb)

        x1, y1, x2, y2 = map(int, face.bbox)
        cropped_face = img[y1:y2, x1:x2]

        person_dir = os.path.join("C:\\Users\\rahul\\OneDrive\\Desktop\\Faces\\known_faces", name)
        os.makedirs(person_dir, exist_ok=True)

        image_count = len(os.listdir(person_dir))
        save_path = os.path.join(person_dir, f"{name}_{image_count+1}.jpg")
        cv2.imwrite(save_path, cropped_face)

        if os.path.exists("embeddings/index.faiss"):
            index = faiss.read_index("embeddings/index.faiss")
            with open("embeddings/labels.pkl", "rb") as f:
                labels = pickle.load(f)
        else:
            index = faiss.IndexFlatIP(512) 
            labels = []

        index.add(np.expand_dims(emb, axis=0))
        labels.append(name)

        faiss.write_index(index, "embeddings/index.faiss")
        with open("embeddings/labels.pkl", "wb") as f:
            pickle.dump(labels, f)
            
    def load_face(self, face_dir):
        self.face_embedding.clear()
        self.face_label.clear()
        for person_name in os.listdir(face_dir):
            path = os.path.join(face_dir, person_name)
            if not os.path.isdir(path):
                continue
            
            for filename in os.listdir(path):      
                img_path = os.path.join(path, filename) 
                img = cv2.imread(img_path)
                if img is None:
                    print(f"Error reading image {path}")
                    continue
            
                faces = app.get(img)
                for face in faces:
                    emb = face.embedding.astype('float32')
                    emb = emb / np.linalg.norm(emb)
                    self.face_embedding.append(emb)
                    self.face_label.append(person_name)
        
        with open("embeddings/labels.pkl", "wb") as f:
            pickle.dump(self.face_label, f)
        np.save("embeddings/vectors.npy", self.face_embedding)
           
        if self.face_embedding:   
            face_np = np.array(self.face_embedding).astype("float32")
            face_np = face_np / np.linalg.norm(face_np, axis=1, keepdims=True)
            
            index = faiss.IndexFlatIP(512)
            index.add(face_np)
            faiss.write_index(index,"embeddings/index.faiss")
            print(f"Loaded {len(self.face_label)} faces into FAISS index.")
        else:
            print("No faces loaded into memory.")
  

    
