from customtkinter import *
from tkinter.messagebox import showerror
from pm import passwordManager
import os
import time
from threading import Thread

pm = passwordManager()


def deleteSite_caller():
    deleteThread = Thread(target=p_m.deleteSite)
    deleteThread.start()


def addPwd_caller():
    loadKeyThread = Thread(target=p_m.addPassword)
    loadKeyThread.start()


class password_manager:

    def __init__(self):
        # start
        self.window = CTk()
        self.window.geometry('1000x800')
        self.window.title('Password Manager')
        self.window.resizable(False, False)
        set_appearance_mode('dark')

        # attributes....
        self.deleteButton = None
        self.deleteSiteEntry = None
        self.optionSite = None
        self.buttonAddPassword = None
        self.entryPass = None
        self.entryEmail = None
        self.entrySite = None
        self.labelP = None
        self.labelE = None
        self.labelS = None
        self.labelLoadPassFile = None
        self.labelLoadKey = None
        self.buttonLoadPassFile = None
        self.buttonCreatePassFile = None
        self.buttonCreateKey = None
        self.buttonLoadKey = None
        self.frameSubmit = None
        self.frameP = None
        self.frameE = None
        self.frameS = None
        self.frameLeft = None

        self.keyPath = None
        self.passwordPath = None
        self.existenceKeyChecker: bool = False
        self.existencePFileChecker: bool = False
        self.checkIfKeyIsLoaded: bool = False

    def loadKey(self):

        fileD = filedialog.askopenfilename(title='uploading key file',
                                           filetypes=(("key file", "*.key"),
                                                      ('All files', '*.*')))
        pm.load_key(fileD)

        if os.path.exists(fileD):
            self.labelLoadKey.configure(text='key found!', fg_color='green4')
            self.existenceKeyChecker = True
            self.checkIfKeyIsLoaded = True
            self.window.update()

        if (self.existencePFileChecker is True) and (self.existenceKeyChecker is True):
            self.buttonAddPassword.configure(state=NORMAL)

    def loadPassFile(self):

        openFilePath = filedialog.askopenfilename(title='opening password file',
                                                  filetypes=(("key file", "*.txt"),
                                                             ('All files', '*.*')))
        pm.load_passwordFile(openFilePath)

        if pm.checkKeyValidility:
            if os.path.exists(openFilePath) and self.checkIfKeyIsLoaded:
                self.labelLoadPassFile.configure(text='file found!', fg_color='green4')
                self.existencePFileChecker = True
                self.window.update()

            if (self.existencePFileChecker is True) and (self.existenceKeyChecker is True):
                sites: list = pm.getAllSites()
                self.buttonAddPassword.configure(state=NORMAL)
                self.optionSite.configure(state=NORMAL, values=sites)
                self.deleteButton.configure(state=NORMAL)

    @staticmethod
    def createKey():
        savePathFile = filedialog.asksaveasfilename(title='creating key file',
                                                    filetypes=(("key file", "*.key"),
                                                               ('All files', '*.*')))
        if len(savePathFile) != 0:
            pm.create_key(savePathFile + '.key')

    def addPassword(self):
        email = str(self.entryEmail.get()).strip()
        password = str(self.entryPass.get()).strip()
        site = str(self.entrySite.get()).strip()

        if (len(email) != 0) and (len(password) != 0) and (len(site) != 0) and ("@" in email) and ("." in email):
            if (site.isspace() is False) and (password.isspace() is False) and (email.isspace() is False):
                pm.add_password(site, email, password)
                sites: list = pm.getAllSites()
                self.optionSite.configure(values=sites)

                self.buttonAddPassword.configure(fg_color='green4', text='submitted',
                                                 text_color_disabled='white',
                                                 state=DISABLED)

                self.window.update()
                time.sleep(1.5)

                self.buttonAddPassword.configure(fg_color='#1162a8', text='submit', hover_color='#013f75', state=NORMAL)
        else:
            self.buttonAddPassword.configure(fg_color='red4', text='invalid input',
                                             text_color_disabled='white',
                                             state=DISABLED)

            self.window.update()
            time.sleep(1.5)

            self.buttonAddPassword.configure(fg_color='#1162a8', text='submit', hover_color='#013f75', state=NORMAL)

    def getPassword(self, choice):
        try:
            arr: list[str] = pm.get_password(choice)
            self.labelS.configure(text=f'Site:      {arr[0]}')
            self.labelE.configure(text=f'Email:     {arr[1]}')
            self.labelP.configure(text=f'Password:  {arr[2]}')
            self.window.update()
        except TypeError:
            showerror('Key error ', '!!!Invalid key to edcrypt!!!')

    @staticmethod
    def createPassFile():
        saveFilePath = filedialog.asksaveasfilename(title='creating password file',
                                                    filetypes=(("text file", "*.txt"),
                                                               ('All files', '*.*')))
        if len(saveFilePath) != 0:
            pm.create_passwordFile(saveFilePath + '.txt')

    def deleteSite(self):
        if (not str(self.deleteSiteEntry.get()).isspace()) and (str(self.deleteSiteEntry.get()) != ''):
            pm.delete_site(self.deleteSiteEntry.get())

            self.deleteButton.configure(fg_color='orange4', text='deleted',
                                        text_color_disabled='white',
                                        state=DISABLED)

            self.window.update()
            time.sleep(1.5)

            self.deleteButton.configure(fg_color='#1162a8', text='delete', hover_color='#013f75', state=NORMAL)
        else:
            self.deleteButton.configure(fg_color='red4', text='invalid input',
                                        text_color_disabled='white',
                                        state=DISABLED)

            self.window.update()
            time.sleep(1.5)

            self.deleteButton.configure(fg_color='#1162a8', text='delete', hover_color='#013f75', state=NORMAL)

        sites: list = pm.getAllSites()
        self.optionSite.configure(values=sites)

    def main(self):

        # Frames--------------------------------------------------------------------------------------------------------
        self.frameLeft = CTkFrame(self.window,
                                  fg_color='gray6',
                                  height=800,
                                  width=300,
                                  corner_radius=False)
        self.frameLeft.pack(side='left')

        self.frameS = CTkFrame(self.window,
                               fg_color='gray6',
                               height=70,
                               width=640,
                               corner_radius=10)
        self.frameS.place(relx=0.33, rely=0.05)

        self.frameE = CTkFrame(self.window,
                               fg_color='gray6',
                               height=70,
                               width=640,
                               corner_radius=10)
        self.frameE.place(relx=0.33, rely=0.17)

        self.frameP = CTkFrame(self.window,
                               fg_color='gray6',
                               height=70,
                               width=640,
                               corner_radius=10)
        self.frameP.place(relx=0.33, rely=0.29)

        self.frameSubmit = CTkFrame(self.window,
                                    fg_color='gray6',
                                    height=450, width=640,
                                    corner_radius=10)
        self.frameSubmit.place(relx=0.33, rely=0.41)

        # buttons and labels in FrameLeft-------------------------------------------------------------------------------
        self.buttonLoadKey = CTkButton(self.frameLeft,
                                       width=150,
                                       height=30,
                                       text='Load key file',
                                       command=p_m.loadKey)
        self.buttonLoadKey.place(relx=0.303, rely=0.1, anchor=CENTER)

        self.buttonCreateKey = CTkButton(self.frameLeft,
                                         width=150,
                                         height=30,
                                         text='Create Key file',
                                         command=p_m.createKey)
        self.buttonCreateKey.place(relx=0.500, rely=0.89, anchor=CENTER)

        self.buttonCreatePassFile = CTkButton(self.frameLeft,
                                              width=150,
                                              height=30,
                                              text='Create password file',
                                              command=p_m.createPassFile)
        self.buttonCreatePassFile.place(relx=0.500, rely=0.74, anchor=CENTER)

        self.buttonLoadPassFile = CTkButton(self.frameLeft,
                                            width=150,
                                            height=30,
                                            text='Load password file',
                                            command=p_m.loadPassFile)
        self.buttonLoadPassFile.place(relx=0.303, rely=0.25, anchor=CENTER)

        self.labelLoadKey = CTkLabel(self.frameLeft,
                                     text='required',
                                     width=107,
                                     height=31,
                                     fg_color='red4',
                                     text_color='white',
                                     corner_radius=5,
                                     font=(None, 17))
        self.labelLoadKey.place(relx=0.775, rely=0.1, anchor=CENTER)

        self.labelLoadPassFile = CTkLabel(self.frameLeft,
                                          text='required',
                                          width=107,
                                          height=31,
                                          fg_color='red4',
                                          text_color='white',
                                          corner_radius=5,
                                          font=(None, 17))
        self.labelLoadPassFile.place(relx=0.775, rely=0.25, anchor=CENTER)

        # labels for the password revealing ----------------------------------------------------------------------------
        self.labelS = CTkLabel(self.frameS,
                               text='Site:',
                               font=('consolas', 20))
        self.labelS.place(relx=0.05, rely=0.28)

        self.labelE = CTkLabel(self.frameE,
                               text='Email:',
                               font=('consolas', 20))
        self.labelE.place(relx=0.05, rely=0.28)

        self.labelP = CTkLabel(self.frameP,
                               text='Password:',
                               font=('consolas', 20))
        self.labelP.place(relx=0.05, rely=0.28)

        # entryBlock----------------------------------------------------------------------------------------------------
        self.entrySite = CTkEntry(self.frameSubmit,
                                  width=400,
                                  height=40,
                                  placeholder_text='Add site',
                                  font=(None, 15),
                                  corner_radius=10)
        self.entrySite.place(relx=0.04, rely=0.06)

        self.entryEmail = CTkEntry(self.frameSubmit,
                                   width=400,
                                   height=40,
                                   placeholder_text='Add email',
                                   font=(None, 15),
                                   corner_radius=10)
        self.entryEmail.place(relx=0.04, rely=0.18)

        self.entryPass = CTkEntry(self.frameSubmit,
                                  width=400,
                                  height=40,
                                  placeholder_text='Add password',
                                  font=(None, 15),
                                  corner_radius=10)
        self.entryPass.place(relx=0.04, rely=0.3)

        self.buttonAddPassword = CTkButton(self.frameSubmit,
                                           text='submit',
                                           height=30, width=170,
                                           corner_radius=6,
                                           font=(None, 19),
                                           state=DISABLED,
                                           command=addPwd_caller)
        self.buttonAddPassword.place(relx=0.04, rely=0.42)

        # optionMenu----------------------------------------------------------------------------------------------------
        self.optionSite = CTkOptionMenu(self.frameSubmit,
                                        height=34, width=170,
                                        values=['Choose'],
                                        dynamic_resizing=False,
                                        font=(None, 15),
                                        state=DISABLED,
                                        command=p_m.getPassword)
        self.optionSite.place(relx=0.7, rely=0.065)

        # delete Site---------------------------------------------------------------------------------------------------
        self.deleteSiteEntry = CTkEntry(self.frameSubmit,
                                        width=300, height=40,
                                        placeholder_text='Delete site',
                                        font=(None, 15),
                                        corner_radius=10)
        self.deleteSiteEntry.place(relx=0.04, rely=0.62)

        self.deleteButton = CTkButton(self.frameSubmit,
                                      text='Delete',
                                      height=30, width=170,
                                      corner_radius=6,
                                      font=(None, 19),
                                      state=DISABLED,
                                      command=deleteSite_caller)
        self.deleteButton.place(relx=0.04, rely=0.74)

        # looping
        self.window.mainloop()


p_m = password_manager()

if __name__ == '__main__':
    p_m.main()
