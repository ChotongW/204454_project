############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
from datetime import timedelta

import time
from PIL import ImageFont
from PIL import ImageDraw
import codecs


######################################## FUNCTION ###############################################


def clear():
    txt.delete(0, "end")
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, "end")
    res = ""
    message.configure(text=res)


def tvInsert(id, date, timestamp):

    with open("StudentDetails\StudentDetails.csv", "r") as studentFile:
        reader2 = csv.reader(studentFile)
        iidd = str(id) + "   "
        # if item['id'] in existing_ids:
        #     return
        # # Add the new item to the treeview
        # existing_ids.add(item['id'])
        # treeview.insert('', 'end', values=(item['id'], item['name'], item['age']))
        for row in reader2:
            if row:
                clean_reader2 = [column.strip() for column in row]
                # print(clean_reader2)
                if clean_reader2[0] == str(id):
                    name = clean_reader2[2]
                    break
                    # print(name)
        tv.insert(
            "",
            0,
            text=iidd,
            values=(
                str(name),
                str(date),
                str(timestamp),
            ),
        )
    studentFile.close()


def csv_Init_tv():
    col_names = ["Id", "", "Name", "", "Date", "", "Time", ""]
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        None
    else:
        with open("Attendance\Attendance_" + date + ".csv", "a+") as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", "r") as csvFile1:
        next(csvFile1)
        # next(csvFile1)
        reader = csv.reader(csvFile1)
        # csv_date = None
        # csv_time = None
        row_count = sum(1 for row in reader)
        csvFile1.seek(0)
        next(csvFile1)
        # reader = csv.reader(csvFile1)
        # print(row_count)
        if row_count > 1:
            with open("StudentDetails\StudentDetails.csv", "r") as studentFile:
                name = ""
                reader2 = csv.reader(studentFile)

                lines = [l.strip() for l in csvFile1.readlines()]
                for line in lines:
                    if line:
                        fields = line.split(",")
                        # print(fields)
                        # print(type(fields))
                        info_id = fields[0]
                        iidd = str(info_id) + "   "
                        csv_date = fields[3]
                        csv_time = fields[5]
                        for row in reader2:
                            if row:
                                clean_reader2 = [column.strip()
                                                 for column in row]
                                # print(clean_reader2)
                                if clean_reader2[0] == str(info_id):
                                    name = clean_reader2[2]
                                    break
                                    # print(name)
                        tv.insert(
                            "",
                            0,
                            text=iidd,
                            values=(
                                str(name),
                                str(csv_date),
                                str(csv_time),
                            ),
                        )
            studentFile.close()
        else:
            return

    csvFile1.close()


def TakeImages():

    # check Id and name
    if (txt.get() == "") or (txt2.get() == ""):
        res = "Please enter Id and Name"
        message.configure(text=res)
        return
    cap = cv2.VideoCapture(0)
    sampleNum = 0
    # take image for learning
    while True:
        start_time = time.time()

        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        Id = txt.get()
        name = txt2.get()
        face_cascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml"
        )  # from git hub https://github.com/opencv/opencv/tree/master/data/haarcascades
        faces = face_cascade.detectMultiScale(gray, 1.05, 5)
        # print(faces)
        # print(type(faces))
        for (x, y, w, h) in faces:
            # drawing rectangle for face
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # incrementing sample number
            sampleNum = sampleNum + 1
            # saving the captured face in the dataset folder TrainingImage
            cv2.imwrite(
                "dataset/User." + Id + "." + str(sampleNum) + ".jpg",
                gray[y: y + h, x: x + w],
            )
        # display the frame
        fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time))
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, fpsInfo, (10, 20), font, 0.4, (255, 255, 255), 1)
        cv2.imshow("Taking Images", img)
        # wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord("q"):
            break
        # break if the sample number is morethan 100
        elif sampleNum > 200:
            break

    cap.release()
    cv2.destroyAllWindows()

    res = "Images Taken for ID : " + Id
    row = [Id, "", name]
    with open("StudentDetails\StudentDetails.csv", "a+", encoding="cp874") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    message1.configure(text=res)


# def TrainImages():
#     recognizer = (
#         cv2.face.LBPHFaceRecognizer_create()
#     )  # recognizer = cv2.face.createLBPHFaceRecognizer()
#     harcascadePath = "haarcascade_frontalface_default.xml"
#     detector = cv2.CascadeClassifier(harcascadePath)
#     faces, Id = getImagesAndLabels("dataset")
#     Id = np.array(Id, dtype=np.int32) # convert Id to numpy array of integers
#     recognizer.train(faces, np.array(Id))
#     recognizer.save("TrainingImageLabel\Trainner.yml")
#     res = "Image Trained"  +",".join(str(f) for f in Id)
#     message.configure(text=res)


def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Ids = getImagesAndLabels("dataset")
    recognizer.train(faces, np.array(Ids))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained" + ",".join(str(f) for f in Ids)
    message.configure(text=res)
    return faces, Ids


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids  # Load images and labels
    # faces = []
    # labels = []
    # for root, dirs, files in os.walk("TrainingImage"):
    #     for file in files:
    #         if file.endswith("png") or file.endswith("jpg"):
    #             path = os.path.join(root, file)
    #             label = int(os.path.basename(root))
    #             img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    #             faces.append(img)
    #             labels.append(label)

    # return faces, labels


def psw():
    global key
    key = tsd.askstring("Password", "Enter Password", show="*")
    if key == "1234":
        res = "Login Success"
        message.configure(text=res)
    else:
        res = "Login Failed"
        message.configure(text=res)


def TrackImages():
    # recognizer for face detection

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    # else:
    #     mess._show(title='?????????????????????????????????', message='????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????!!')
    #     return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    faces, Ids = TrainImages()

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ["Id", "", "Name", "", "Date", "", "Time", ""]
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title="?????????????????????????????????????????????",
                   message="????????????????????????????????????????????????????????????????????????????????????????????????!")
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        None
    else:
        with open("Attendance\Attendance_" + date + ".csv", "a+") as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
        csvFile1.close()

    while True:
        # varible for cathing attendance
        is_checked = False
        ret, im = cam.read()

        start_time = time.time()
        # if (nowTime - startTime) > 0.01:
        # TrainImages()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.05, 5, minSize=(20, 20))
        # TrainImages()
        # bb = ''
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            gray_face = gray[y: y + h, x: x + w]
            label, conf = recognizer.predict(gray_face)
            if conf < 50:
                # print(conf)
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime("%H:%M:%S")
                # ID = str(ID)
                # ID = ID[1:-1]
                # bb = bb[2:-2]
                # print(faces1)
                ID = label
                # ID = "unknown"
                # print(label)
                # print(bb)
                # bb = str(df.loc[df['Id'] == int(ID)]['Name'].values)
                if conf < 40:
                    attendance = [
                        str(ID),
                        "",
                        # bb,
                        "",
                        str(date),
                        "",
                        str(timeStamp),
                        "",
                    ]
                    with open(
                        "Attendance\Attendance_" + date + ".csv", "r"
                    ) as csvFile1:
                        next(csvFile1)
                        # next(csvFile1)
                        reader = csv.reader(csvFile1)
                        # csv_date = None
                        # csv_time = None
                        row_count = sum(1 for row in reader)
                        csvFile1.seek(0)
                        next(csvFile1)
                        # reader = csv.reader(csvFile1)
                        # print(row_count)
                        if row_count > 1:

                            lines = [l.strip() for l in csvFile1.readlines()]
                            for line in lines:
                                if line:
                                    fields = line.split(",")
                                    # print(fields)
                                    # print(type(fields))
                                    info_id = int(fields[0])
                                    # print(info_id)
                                    # print(ID)
                                    if info_id == ID:
                                        is_checked = True
                                        # csv_date = fields[3]
                                        # csv_time = fields[5]
                                        # print("call")
                                        break

                        else:
                            None
                    csvFile1.close()
                    # put attendance in csv file
                    with open(
                        "Attendance\Attendance_" + date + ".csv", "a+"
                    ) as csvFile1:
                        writer = csv.writer(csvFile1)
                        if is_checked == False:
                            writer.writerow(attendance)
                            print("attendance checked already")
                            tvInsert(attendance[0],
                                     attendance[3], attendance[5])
                            # is_checked = True
                        else:
                            # csv_time = datetime.datetime.strptime(csv_time, "%H:%M:%S")
                            # timeCompare = datetime.datetime.strptime(
                            #     timeStamp, "%H:%M:%S"
                            # )
                            # if date == csv_date:
                            #     print(type(timeCompare), type(csv_time))
                            #     time_diff = timeCompare - csv_time
                            #     print(time_diff)
                            #     if time_diff > timedelta(hours=8):
                            #         print("Timestamp is greater than 8 hours ago")

                            #     # elif timestamp < start_time or timestamp > end_time:

                            #     # if timeStamp - csv_time < 8:

                            #     # print(timeStamp - csv_time)
                            # print("You already cheked")
                            # create_popup_checked
                            mess._show(
                                title="checked",
                                message="You are already checked for this day!!",
                            )

                        # writer.writerow(attendance)
                    csvFile1.close()
                    cv2.imshow("Taking Attendance", im)

            else:
                # print(conf)
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime("%H:%M:%S")
                timeStamp1 = datetime.datetime.fromtimestamp(
                    ts).strftime("%H-%M-%S")
                # ID =label
                ID = "unknown"
                # ID = ID[1:-1]
                # bb = "Undefined"
                # ID = str(Ids[label])
                # bb = str(df.loc[df['Id'] == int(ID)]['Name'].values)

                # if conf > 75:

                #     attendance = [
                #         str(ID),
                #         "",
                #         # bb,
                #         "",
                #         str(date),
                #         "",
                #         str(timeStamp),
                #         "",
                #     ]

            cv2.putText(im, str(ID), (x, y + h), font, 1, (255, 255, 255), 2)

        fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time))
        font = cv2.FONT_HERSHEY_DUPLEX

        cv2.putText(im, fpsInfo, (10, 20), font, 0.4, (255, 255, 255), 1)
        startTime = time.time()

        cv2.imshow("Taking Attendance", im)
        if cv2.waitKey(1) == ord("q"):
            break

    # with open("Attendance\Attendance_" + date + ".csv", "r") as csvFile1:
    #     reader1 = csv.reader(csvFile1)
    #     i = 0
    #     for lines in reader1:
    #         i = i + 1
    #         if i > 1:
    #             if i % 2 != 0:
    #                 iidd = str(lines[0]) + "   "
    #                 tv.insert(
    #                     "",
    #                     0,
    #                     text=iidd,
    #                     values=(
    #                         str(lines[2]),
    #                         str(lines[4]),
    #                         str(lines[6]),
    #                         str(lines[8]),
    #                     ),
    #                 )
    # csvFile1.close()

    cam.release()
    cv2.destroyAllWindows()


######################################## USED STUFFS ############################################

global key
key = ""

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
day, month, year = date.split("-")

mont = {
    "01": "??????????????????",
    "02": "??????????????????????????????",
    "03": "??????????????????",
    "04": "??????????????????",
    "05": "?????????????????????",
    "06": "????????????????????????",
    "07": "?????????????????????",
    "08": "?????????????????????",
    "09": "?????????????????????",
    "10": "??????????????????",
    "11": "???????????????????????????",
    "12": "?????????????????????",
}
##################################################################################


def tick():
    time_string = time.strftime("%H:%M:%S")
    clock.config(text=time_string)
    clock.after(200, tick)


######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, False)
window.title("????????????????????????????????????????????? ??????????????????????????????")
window.configure(background="#262523")

frame1 = tk.Frame(window, bg="#00ffca")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#00ffca")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(
    window,
    text="????????????????????????????????????????????? ??????????????????????????????",
    fg="white",
    bg="#262523",
    width=55,
    height=1,
    font=("times", 29, " bold "),
)
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(
    frame4,
    text=" " + day + " " + mont[month] + " " + year + "  |  ",
    fg="orange",
    bg="#262523",
    width=55,
    height=1,
    font=("times", 20, " bold "),
)
datef.pack(fill="both", expand=1)

clock = tk.Label(
    frame3, fg="orange", bg="#262523", width=55, height=1, font=("times", 22, " bold ")
)
clock.pack(fill="both", expand=1)
tick()

head2 = tk.Label(
    frame2,
    text="                        ?????????????????????????????????????????????                             ",
    fg="black",
    bg="#3ece48",
    font=("times", 17, " bold "),
)
head2.grid(row=0, column=0)

head1 = tk.Label(
    frame1,
    text="                              ??????????????????????????????                               ",
    fg="black",
    bg="#3ece48",
    font=("times", 17, " bold "),
)
head1.place(x=0, y=0)

lbl = tk.Label(
    frame2,
    text="????????????",
    width=20,
    height=1,
    fg="black",
    bg="#00ffca",
    font=("times", 17, " bold "),
)
lbl.place(x=80, y=55)

txt = tk.Entry(frame2, width=32, fg="black",
               bg="white", font=("times", 15, " bold "))
txt.place(x=30, y=88)

lbl2 = tk.Label(
    frame2,
    text="???????????? ?????????????????????",
    width=20,
    fg="black",
    bg="#00ffca",
    font=("times", 17, " bold "),
)
lbl2.place(x=80, y=140)

txt2 = tk.Entry(
    frame2, width=32, fg="black", bg="white", font=("Courier", 15, " bold ")
)
txt2.place(x=30, y=173)

message1 = tk.Label(
    frame2,
    text="1)?????????????????????  >>>  2)????????????????????????????????????",
    bg="#00ffca",
    fg="black",
    width=39,
    height=1,
    activebackground="yellow",
    font=("times", 15, " bold "),
)
message1.place(x=7, y=230)

message = tk.Label(
    frame2,
    text="",
    bg="#00ffca",
    fg="black",
    width=39,
    height=1,
    activebackground="yellow",
    font=("times", 16, " bold "),
)
message.place(x=7, y=450)

lbl3 = tk.Label(
    frame1,
    text="??????????????????",
    width=20,
    fg="black",
    bg="#00ffca",
    height=1,
    font=("times", 17, " bold "),
)
lbl3.place(x=100, y=115)

# res=0
# exists = os.path.isfile("StudentDetails\StudentDetails.csv")
# if exists:
#     with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
#         reader1 = pd.read_csv(csvFile1,encoding='utf-8')
#         for l in reader1:
#             res = res + 1
#     res = (res // 2)
#     csvFile1.close()
# else:
#     res = 0
# message.configure(text='????????????????????????????????????????????????????????????  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window, relief="ridge")
filemenu = tk.Menu(menubar, tearoff=0)
# filemenu.add_command(label='?????????????????????????????????', command = change_pass)
# filemenu.add_command(label='??????????????????', command = contact)
filemenu.add_command(label="?????????", command=window.destroy)
menubar.add_cascade(label="?????????????????????", font=(
    "times", 29, " bold "), menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv = ttk.Treeview(frame1, height=13, columns=("name", "date", "time"))
tv.column("#0", width=75)
tv.column("name", width=110)
tv.column("date", width=110)
tv.column("time", width=110)
tv.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=3)
tv.heading("#0", text="????????????")
tv.heading("name", text="????????????")
tv.heading("date", text="??????????????????")
tv.heading("time", text="????????????")
csv_Init_tv()


###################### SCROLLBAR ################################

scroll = ttk.Scrollbar(frame1, orient="vertical", command=tv.yview)
scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky="ns")
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(
    frame2,
    text="??????",
    command=clear,
    fg="black",
    bg="#ea2a2a",
    width=11,
    activebackground="white",
    font=("times", 11, " bold "),
)
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(
    frame2,
    text="??????",
    command=clear2,
    fg="black",
    bg="#ea2a2a",
    width=11,
    activebackground="white",
    font=("times", 11, " bold "),
)
clearButton2.place(x=335, y=172)
takeImg = tk.Button(
    frame2,
    text="?????????????????????",
    command=TakeImages,
    fg="black",
    bg="blue",
    width=34,
    height=1,
    activebackground="white",
    font=("times", 15, " bold "),
)
takeImg.place(x=30, y=300)
trainImg = tk.Button(
    frame2,
    text="????????????????????????????????????",
    command=psw,
    fg="black",
    bg="blue",
    width=34,
    height=1,
    activebackground="white",
    font=("times", 15, " bold "),
)
trainImg.place(x=30, y=380)
trackImg = tk.Button(
    frame1,
    text="???????????????????????????",
    command=TrackImages,
    fg="black",
    bg="yellow",
    width=35,
    height=1,
    activebackground="white",
    font=("times", 15, " bold "),
)
trackImg.place(x=30, y=50)
quitWindow = tk.Button(
    frame1,
    text="???????????????????????????????????????",
    command=window.destroy,
    fg="black",
    bg="red",
    width=35,
    height=1,
    activebackground="white",
    font=("times", 15, " bold "),
)
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
