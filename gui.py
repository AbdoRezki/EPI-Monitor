from tkinter import *
import customtkinter 
import cv2 
from PIL import Image, ImageTk 
from ultralytics import YOLO 
import time 
import json 
customtkinter.set_appearance_mode("dark") 
class App(customtkinter.CTk): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.title("Détection des EPIs") 
        self.geometry("1250x700") 
        self.detections={"mask":"Not detected","glasses":"Not detected","hardHat":"Not detected","vest":"Not detected"} 
        self.cap = cv2.VideoCapture(0) 
        self.cap.set(3, 650) 
        self.cap.set(4, 500) 
        self.side_left = customtkinter.CTkFrame(master=self, width=250) 
        self.side_left.pack(side="left", padx=10,pady=10, fill="both") 
        self.side_right = customtkinter.CTkFrame(master=self, width=250) 
        self.side_right.pack(side="right",padx=10,pady=10,fill="both", expand=False) 
        self.side_left_label = customtkinter.CTkLabel(master=self.side_left, text="Détection des EPIs \n en temps réel", font=("Arial",20,'bold')) 
        self.side_left_label.place(relx=0.5, rely=0.1, anchor=CENTER) 
        self.glass_button = customtkinter.CTkButton(master=self.side_left, width= 200, height= 40, font=("Arial",17), hover_color="red4", fg_color="red3", text="Détecter les lunettes",command=self.showGlassFrame) 
        self.glass_button.place(relx=0.5,rely=0.3,anchor=CENTER) 
        self.hard_hat_detect_button = customtkinter.CTkButton(master=self.side_left, width= 200, height= 40, font=("Arial",17), hover_color="red4", fg_color="red3", text="Détecter le casque de sécurité",command=self.showHardHatFrame) 
        self.hard_hat_detect_button.place(relx=0.5,rely=0.37,anchor=CENTER) 
        self.mask_detect_button = customtkinter.CTkButton(master=self.side_left, width= 200, height= 40, font=("Arial",17), hover_color="red4", fg_color="red3", text="Détecter le masque",command=self.showMaskFrame) 
        self.mask_detect_button.place(relx=0.5,rely=0.44,anchor=CENTER) 
        self.safety_vest_button = customtkinter.CTkButton(master=self.side_left, width= 200, height= 40, font=("Arial",17), hover_color="red4", fg_color="red3", text="Détecter le gilet de sécurité",command=self.showVestFrame) 
        self.safety_vest_button.place(relx=0.5,rely=0.51,anchor=CENTER) 
        self.side_right_label = customtkinter.CTkLabel(master=self.side_right, text="Résultats des détections", font=("Arial",20,'bold')) 
        self.side_right_label.place(relx=0.5, rely=0.1, anchor=CENTER) 
        self.hard_hat_detected = customtkinter.CTkLabel(master=self.side_right, text="Aucun casque détecté", font=("Arial",19,'bold'), text_color="red") 
        self.hard_hat_detected.place(relx=0.5, rely=0.3, anchor=CENTER) 
        self.mask_detected = customtkinter.CTkLabel(master=self.side_right, text="Aucun masque détecté", font=("Arial",19,'bold'), text_color="red") 
        self.mask_detected.place(relx=0.5, rely=0.35, anchor=CENTER) 
        self.safety_vest_detected = customtkinter.CTkLabel(master=self.side_right, text="Aucun gilet détecté", font=("Arial",19,'bold'), text_color="red") 
        self.safety_vest_detected.place(relx=0.5, rely=0.4, anchor=CENTER) 
        self.safety_glasses_detected = customtkinter.CTkLabel(master=self.side_right, text="Aucune lunette détectée", font=("Arial",19,'bold'), text_color="red") 
        self.safety_glasses_detected.place(relx=0.5, rely=0.45, anchor=CENTER) 
        self.main_frame = customtkinter.CTkFrame(master=self) 
        self.main_frame.pack(padx=10,pady=10,fill="both", expand=True) 
        self.model = YOLO("C:/Users/abrezki/Desktop/NLP/helmet/PPE_detection.pt") 
        self.model_glasses = YOLO("C:/Users/abrezki/Desktop/NLP/helmet/glasses.pt") 
        # self.model = YOLO("models/PPE_detection.pt") # self.model_glasses = YOLO("models/glasses.pt") # self.model = YOLO("/opt/testIA/pytonscripts/models/PPE_detection.pt") # self.model_glasses = YOLO("/opt/testIA/pytonscripts/models/glasses.pt") 
    def showGlassFrame(self): 
        self.glass_frame = customtkinter.CTkFrame(master=self) 
        self.glass_label = customtkinter.CTkLabel(master=self.glass_frame, text="Détection de lunettes", font=("Arial",20), width=500, height=1000) 
        self.glass_label.place(relx=0.5, rely=0.1, anchor=CENTER) 
        self.camera_label = customtkinter.CTkLabel(master=self.glass_frame, justify="center", font=("Arial",17), text="""Cliquez sur le bouton « Ouvrir la caméra » et attendez que la caméra apparaisse. Une fois affiché, vous devrez attendre un peu jusqu'à ce que votre objet soit détecté sur le cadre latéral droit. Vous pouvez également basculer entre les écrans sans devoir fermer la caméra.""") 
        self.camera_label.place(relx=0.5, rely=0.5, anchor=CENTER) 
        self.glass_button = customtkinter.CTkButton(master=self.glass_frame, width= 200, height= 40, font=("Arial",17), hover_color="red4", fg_color="red3", text="Ouvrir la caméra", command=self.start_timer_glass) 
        self.glass_button.place(relx=0.5,rely=0.85,anchor=CENTER) 
        self.main_frame.destroy() 
        self.main_frame = self.glass_frame 
        self.main_frame.pack(padx=10,pady=10,fill="both", expand=True) 
    def showMaskFrame(self): 
        self.mask_frame = customtkinter.CTkFrame(master=self) 
        self.mask_label = customtkinter.CTkLabel(master=self.mask_frame, text="Détection de masque", font=("Arial",20), width=500, height=1000) 
        self.mask_label.place(relx=0.5, rely=0.1, anchor=CENTER) 
        self.camera_label = customtkinter.CTkLabel(master=self.mask_frame, justify="center", font=("Arial",17), text="""Cliquez sur le bouton « Ouvrir la caméra » et attendez que la caméra apparaisse. Une fois affiché, vous devrez attendre un peu jusqu'à ce que votre objet soit détecté sur le cadre latéral droit. Vous pouvez également basculer entre les écrans sans devoir fermer la caméra.""") 
        self.camera_label.place(relx=0.5, rely=0.5, anchor=CENTER) 
        self.mask_button = customtkinter.CTkButton(master=self.mask_frame, width= 200, height= 40, font=("Arial",17), hover_color="red4", fg_color="red3", text="Ouvrir la caméra", command=self.start_timer_mask) 
        self.mask_button.place(relx=0.5,rely=0.85,anchor=CENTER) 
        self.main_frame.destroy() 
        self.main_frame = self.mask_frame 
        self.main_frame.pack(padx=10,pady=10,fill="both", expand=True) 
    def showVestFrame(self): 
        self.vest_frame = customtkinter.CTkFrame(master=self) 
        self.camera_label = customtkinter.CTkLabel(master=self.vest_frame, justify="center", font=("Arial",17), text="""Cliquez sur le bouton « Ouvrir la caméra » et attendez que la caméra apparaisse. Une fois affiché, vous devrez attendre un peu jusqu'à ce que votre objet soit détecté sur le cadre latéral droit. Vous pouvez également basculer entre les écrans sans devoir fermer la caméra.""") 
        self.camera_label.place(relx=0.5, rely=0.5, anchor=CENTER) 
        self.vest_button = customtkinter.CTkButton(master=self.vest_frame, width= 200, height= 40, font=("Arial",17), hover_color="red4", fg_color="red3", text="Ouvrir la caméra", command=self.start_timer_vest) 
        self.vest_button.place(relx=0.5,rely=0.85,anchor=CENTER) 
        self.vest_label = customtkinter.CTkLabel(master=self.vest_frame, text="Détection des gilets de sécurité", font=("Arial",20)) 
        self.vest_label.place(relx=0.5, rely=0.1, anchor=CENTER) 
        self.main_frame.destroy() 
        self.main_frame = self.vest_frame 
        self.main_frame.pack(padx=10,pady=10,fill="both", expand=True) 
    def showHardHatFrame(self): 
        self.hard_hat_frame = customtkinter.CTkFrame(master=self) 
        self.camera_label = customtkinter.CTkLabel(master=self.hard_hat_frame, justify="center", font=("Arial",17), text="""Cliquez sur le bouton « Ouvrir la caméra » et attendez que la caméra apparaisse. Une fois affiché, vous devrez attendre un peu jusqu'à ce que votre objet soit détecté sur le cadre latéral droit. Vous pouvez également basculer entre les écrans sans devoir fermer la caméra.""") 
        self.camera_label.place(relx=0.5, rely=0.5, anchor=CENTER) 
        self.hard_hat_button = customtkinter.CTkButton(master=self.hard_hat_frame, width= 200, height= 40, font=("Arial",17), hover_color="red4", fg_color="red3", text="Ouvrir la caméra", command= self.start_timer_hard_hat) 
        self.hard_hat_button.place(relx=0.5,rely=0.85,anchor=CENTER) 
        self.hard_hat_label = customtkinter.CTkLabel(master=self.hard_hat_frame, text="Détection des casques de sécurité", font=("Arial",20)) 
        self.hard_hat_label.place(relx=0.5, rely=0.1, anchor=CENTER) 
        self.main_frame.destroy() 
        self.main_frame = self.hard_hat_frame 
        self.main_frame.pack(padx=10,pady=10,fill="both", expand=True) 
    def start_timer_mask(self): 
        self.seconds= time.time() 
        self.showCameraMask() 
    def showCameraMask(self): 
        if not self.cap.read()[0]: 
            self.cap= cv2.VideoCapture(0) 
            self.cap.set(3, 650) 
            self.cap.set(4, 500) 
            _, frame = self.cap.read() 
            results = self.model(frame, verbose=False, stream=True, classes=[1,3]) 
        if(time.time()-self.seconds >= 7): 
            self.mask_detected.configure(text="Masque détecté",text_color="green yellow") 
            self.detections.update({"mask":"Detected"}) 
            for r in results: 
                boxes = r.boxes 
                if(1 not in boxes.cls): 
                    self.seconds=time.time() 
                    for box in boxes: 
                        x1, y1, x2, y2 = box.xyxy[0] 
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 
                        cls = int(box.cls[0]) # object details 
                        org = (x1, y1) 
                        font = cv2.FONT_HERSHEY_SIMPLEX 
                        fontScale = 1 
                        color = (255, 0, 0) 
                        thickness = 2 
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3) 
                        cv2.putText(frame, self.model.names[cls] + " " + "{:.2f}".format(float(box.conf[0])*100)+ "%", org, font, fontScale, color, thickness) # Convert image from one color space to other 
                        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # Capture the latest frame and transform to image 
                        captured_image = Image.fromarray(opencv_image) # Convert captured image to photoimage 
                        photo_image = ImageTk.PhotoImage(image=captured_image) # Displaying photoimage in the label 
                        self.camera_label.photo_image = photo_image # Configure image in the label 
                        self.camera_label.configure(image=photo_image, text="") 
                        self.mask_button.configure(text="Fermer la caméra", command=self.closeCameraMask) # Repeat the same process after every 10 seconds 
                        self.callback = self.camera_label.after(10, self.showCameraMask) 
    def closeCameraMask(self): 
        self.camera_label.configure(image="", justify="center", font=("Arial",17),text="""Cliquez sur le bouton « Ouvrir la caméra » et attendez que la caméra apparaisse. Une fois affiché, vous devrez attendre un peu jusqu'à ce que votre objet soit détecté sur le cadre latéral droit. Vous pouvez également basculer entre les écrans sans devoir fermer la caméra.""") 
        self.mask_button.configure(text="Ouvrir la caméra", command=self.showCameraMask) 
        self.camera_label.after_cancel(self.callback) 
        self.cap.release() 
    def start_timer_vest(self): 
        self.seconds= time.time() 
        self.showCameraVest() 
    def showCameraVest(self): 
        if not self.cap.read()[0]: 
            self.cap= cv2.VideoCapture(0) 
            self.cap.set(3, 650) 
            self.cap.set(4, 500) 
            _, frame = self.cap.read() 
            results = self.model(frame,verbose=False, stream=True, classes=[4,7]) 
            if(time.time()-self.seconds >= 7): 
                self.safety_vest_detected.configure(text="Gilet de sécurité détecté",text_color="green yellow") 
                self.detections.update({"vest":"Detected"}) 
                for r in results: 
                    boxes = r.boxes 
                    if(1 not in boxes.cls): 
                        self.seconds=time.time() 
                        for box in boxes: 
                            x1, y1, x2, y2 = box.xyxy[0] 
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 
                            cls = int(box.cls[0]) # object details 
                            org = (x1, y1) 
                            font = cv2.FONT_HERSHEY_SIMPLEX 
                            fontScale = 1 
                            color = (255, 0, 0) 
                            thickness = 2 
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3) 
                            cv2.putText(frame, self.model.names[cls] + " " + "{:.2f}".format(float(box.conf[0])*100)+ "%", org, font, fontScale, color, thickness) # Convert image from one color space to other 
                            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # Capture the latest frame and transform to image 
                            captured_image = Image.fromarray(opencv_image) # Convert captured image to photoimage 
                            photo_image = ImageTk.PhotoImage(image=captured_image) # Displaying photoimage in the label 
                            self.camera_label.photo_image = photo_image # Configure image in the label 
                            self.camera_label.configure(image=photo_image, text="") 
                            self.vest_button.configure(text="Fermer la caméra", command=self.closeCameraVest) # Repeat the same process after every 10 seconds 
                            self.callback = self.camera_label.after(10, self.showCameraVest) 
    def closeCameraVest(self): 
        self.camera_label.configure(image="", justify="center", font=("Arial",17),text="""Cliquez sur le bouton « Ouvrir la caméra » et attendez que la caméra apparaisse. Une fois affiché, vous devrez attendre un peu jusqu'à ce que votre objet soit détecté sur le cadre latéral droit. Vous pouvez également basculer entre les écrans sans devoir fermer la caméra.""") 
        self.vest_button.configure(text="Ouvrir la caméra", command=self.showCameraVest)
        self.camera_label.after_cancel(self.callback) 
        self.cap.release() 
    def start_timer_glass(self): 
        self.seconds= time.time() 
        self.showCameraGlass() 
    def showCameraGlass(self): 
        if not self.cap.read()[0]: 
            self.cap= cv2.VideoCapture(0) 
            self.cap.set(3, 650) 
            self.cap.set(4, 500) 
            _, frame = self.cap.read() 
            results = self.model_glasses(frame,verbose=False, stream=True) 
            if(time.time()-self.seconds >= 7): 
                self.safety_glasses_detected.configure(text="Lunettes détectées", text_color="green yellow") 
                self.detections.update({"glasses":"Detected"}) 
                for r in results: boxes = r.boxes 
                if(1 not in boxes.cls): 
                    self.seconds=time.time() 
                    for box in boxes: 
                        x1, y1, x2, y2 = box.xyxy[0] 
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 
                        cls = int(box.cls[0]) # object details 
                        org = (x1, y1) 
                        font = cv2.FONT_HERSHEY_SIMPLEX 
                        fontScale = 1 
                        color = (255, 0, 0) 
                        thickness = 2 
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3) 
                        cv2.putText(frame, self.model_glasses.names[cls] + " " + "{:.2f}".format(float(box.conf[0])*100)+ "%", org, font, fontScale, color, thickness) # Convert image from one color space to other 
                        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # Capture the latest frame and transform to image 
                        captured_image = Image.fromarray(opencv_image) # Convert captured image to photoimage 
                        photo_image = ImageTk.PhotoImage(image=captured_image) # Displaying photoimage in the label 
                        self.camera_label.photo_image = photo_image # Configure image in the label 
                        self.camera_label.configure(image=photo_image, text="") 
                        self.glass_button.configure(text="Fermer la caméra", command=self.closeCameraGlass) # Repeat the same process after every 10 seconds 
                        self.callback = self.camera_label.after(10, self.showCameraGlass) 
    def closeCameraGlass(self): 
        self.camera_label.configure(image="", justify="center", font=("Arial",17),text="""Cliquez sur le bouton « Ouvrir la caméra » et attendez que la caméra apparaisse. Une fois affiché, vous devrez attendre un peu jusqu'à ce que votre objet soit détecté sur le cadre latéral droit. Vous pouvez également basculer entre les écrans sans devoir fermer la caméra.""") 
        self.glass_button.configure(text="Ouvrir la caméra", command=self.showCameraGlass) 
        self.camera_label.after_cancel(self.callback) 
        self.cap.release() 
    def start_timer_hard_hat(self): 
        self.seconds= time.time() 
        self.showCameraHardHat() 
    def showCameraHardHat(self): 
        if not self.cap.read()[0]: self.cap= cv2.VideoCapture(0) 
        self.cap.set(3, 650) 
        self.cap.set(4, 500) 
        _, frame = self.cap.read() 
        results = self.model(frame, verbose=False,stream=True, classes=[0,2]) 
        if(time.time()-self.seconds >= 7): 
            self.hard_hat_detected.configure(text="Casque de sécurité détecté",text_color="green yellow") 
            self.detections.update({"hardHat":"Detected"}) 
            for r in results: 
                boxes = r.boxes 
                if(2 in boxes.cls): 
                    self.seconds=time.time() 
                    for box in boxes: 
                        x1, y1, x2, y2 = box.xyxy[0] 
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 
                        cls = int(box.cls[0]) # object details 
                        org = (x1, y1) 
                        font = cv2.FONT_HERSHEY_SIMPLEX 
                        fontScale = 1 
                        color = (255, 0, 0) 
                        thickness = 2 
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3) 
                        cv2.putText(frame, self.model.names[cls] + " " + "{:.2f}".format(float(box.conf[0])*100)+ "%", org, font, fontScale, color, thickness) # Convert image from one color space to other 
                        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) # Capture the latest frame and transform to image 
                        captured_image = Image.fromarray(opencv_image) # Convert captured image to photoimage 
                        photo_image = ImageTk.PhotoImage(image=captured_image) # Displaying photoimage in the label 
                        self.camera_label.photo_image = photo_image # Configure image in the label 
                        self.camera_label.configure(image=photo_image, text="") 
                        self.hard_hat_button.configure(text="Fermer la caméra", command=self.closeCameraHardHat) # Repeat the same process after every 10 seconds 
                        self.callback = self.camera_label.after(10, self.showCameraHardHat) 
    def closeCameraHardHat(self): 
        self.camera_label.configure(image="", justify="center", font=("Arial",17),text="""Cliquez sur le bouton « Ouvrir la caméra » et attendez que la caméra apparaisse. Une fois affiché, vous devrez attendre un peu jusqu'à ce que votre objet soit détecté sur le cadre latéral droit. Vous pouvez également basculer entre les écrans sans devoir fermer la caméra.""") 
        self.hard_hat_button.configure(text="Ouvrir la caméra", command=self.showCameraHardHat) 
        self.camera_label.after_cancel(self.callback) 
        self.cap.release() 
if __name__ == "__main__": 
    app = App() 
    app.mainloop() 
    print(json.dumps(app.detections))