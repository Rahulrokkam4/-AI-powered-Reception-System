from emailutilis import Emailsender
from voive_engine import Voicein
import cv2
import faiss
import pickle
import numpy as np
from face_analyzer import app

assistant = Voicein()
email = Emailsender()


try:
    cap = cv2.VideoCapture(0)
    greeted = set()

    index = faiss.read_index("embeddings/index.faiss")
    with open("embeddings/labels.pkl", "rb") as f:
        labels = pickle.load(f)
    loop_exit = False
    while not loop_exit:
        ret, frame = cap.read()
        if not ret:
            break
    
        # Detect faces and extract embeddings
        faces = app.get(frame)
        for face in faces:
            emb = face.embedding.astype("float32").reshape(1, -1)
            emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)
    
            # Search in FAISS
            D, I = index.search(emb, k=1)  # Get nearest neighbor
            if D[0][0] < 0.6:  # Lower = better match (Euclidean L2)
                name = labels[I[0][0]]
                if name not in greeted:
                    greeted.add(name)

                    assistant.speak(f"Hello {name}, welcome. Who are you here to meet?")
                    purpose = assistant.listen()
                    assistant.speak("wait a momemt i sending mail")
                    employee_name, detail = email.emailretriver(purpose)
                    if employee_name and detail:
                        email.send_email_to_employee(name, employee_name, detail)
                        assistant.speak(f"Email sent to {employee_name} sucessfully")
                    else:
                        assistant.speak("Sorry, I could not find that employee.")   
                        
                loop_exit = True
                    
            else:
                name = "unknown"
                x1, y1, x2, y2 = face.bbox.astype(int)
                unknown_face = frame[y1:y2, x1:x2]
                assistant.speak("hello i don't recognize you! wait a moment i will connect to hr")
                saved_path = email.save_unknown_face(unknown_face)
                email.send_unknown_to_hr(saved_path)
                assistant.speak("i send request to hr. he connect you please wait moment") 
                loop_exit = True
        
            #Draw bounding box and label
            x1, y1, x2, y2 = face.bbox.astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
        # Show result
        cv2.imshow("Face Recognition", frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print("[! ERROR :]",e)
finally:
    cap.release()

    cv2.destroyAllWindows()
