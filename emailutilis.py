import os
import cv2
import smtplib
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()


# employee details
employee_detail = {
    "raghu":"rahulrokkam1234@gmail.com",
    "kumar":"ravikumar3@gmail.com"
}

class Emailsender:
    def __init__(self):
        self.EMAIL_USER = os.getenv("EMAIL_USER")
        self.EMAIL_PASS = os.getenv("EMAIL_PASS")
        self.EMAIL_HOST = os.getenv("EMAIL_HOST")
        self.EMAIL_PORT = os.getenv("EMAIL_PORT")
        self.unknown_face_dir = "C:\\Users\\rahul\\OneDrive\\Desktop\\Faces\\unknown_faces"
        
        
    def send_email_to_employee(self, visitor_name, employee_name, to_email):
        msg = EmailMessage()
        msg["Subject"] = f"Visitor Alert: {visitor_name} is here to meet {employee_name}"
        msg["From"] = self.EMAIL_USER
        msg["To"] = to_email
        msg.set_content(f"{visitor_name} is here to meet you at the reception.")
        try:
            with smtplib.SMTP(self.EMAIL_HOST, 587) as server:
                server.starttls()
                server.login(self.EMAIL_USER, self.EMAIL_PASS)
                server.send_message(msg)
        except Exception as e:
            print(e)
                    
        
    def send_unknown_to_hr(self, image_path):
        msg = EmailMessage()
        msg["Subject"] = "Unknown Visitor Alert"
        msg["From"] = self.EMAIL_USER
        msg["To"] = "rahulrokkam1234@gmail.com"
        msg.set_content("An unknown person visited. Photo is attached.")

        with open(image_path, "rb") as img:
            msg.add_attachment(img.read(), maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

        try:
            with smtplib.SMTP(self.EMAIL_HOST, 587) as server:
                server.starttls()
                server.login(self.EMAIL_USER, self.EMAIL_PASS)
                server.send_message(msg)
        except Exception as e:
            print("[! ERROR sending email:]", e)
        
        
    def emailretriver(self, purpose):
        for name in employee_detail:
            if name.lower() in purpose.lower():
                employee_name = name
                break
        if employee_name:
            return employee_name, employee_detail[employee_name]
        else:
            return None, None
        
    def save_unknown_face(self, face_img):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"unknown_visitor_{timestamp}.jpg"
        save_path = os.path.join(self.unknown_face_dir, filename)
        os.makedirs(self.unknown_face_dir, exist_ok=True)
        cv2.imwrite(save_path, face_img)
        return save_path


if __name__ == "__main__":
    e = Emailsender()
    e.send_email_to_employee("rahul","kumar","ravirokkam3@gmail.com")
    