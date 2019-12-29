##################################################
##                                              ##
##  Python Code = Intern - Danish Naseem        ##
##  Bash Code = Matt Crnich                     ##
##  Dog Photo Credit = Derek Viramontes         ##
##                                              ##
##  FCB Chicago (Lord and Thomas)               ##
##  Lord and Thomas Universal Encoder           ##
##                                              ##
##  Date Created = 06/22/2018                   ##
##  Date Modified = 04/18/2019                  ##
##                                              ##
##  Copyright = Copyright © 2019 Danish Naseem  ##
##  Version = 2.0                               ##
##                                              ##
##################################################

############################################### FOR REFERENCE PURPOSES: #####################################################
#                                                                                                                           #
#   ## VIDEO FORMATS ##                                                                                                     #
#                                                                                                                           #
#   ('.webm', '.mov', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.ogg', '.mp4', '.m4p', '.m4v', '.mxf')                      #
#                                                                                                                           #
#   #########################################################################################                               #
#                                                                                                                           #
#   ## BASH CODES ##                                                                                                        #
#                                                                                                                           #
#   # ffmpeg mov encoder #                                                                                                  #
#                                                                                                                           #
#   /Volumes/Agency-1/LT-Tools/_ffmpeg/ffmpeg -i "/input/dir" -map 0 -c copy -c:v libx264 -preset medium -tune              #
#   fastdecode -vf scale=1920:-1 -pix_fmt yuv420p -movflags +faststart /dst/dir/file_name;.mov                              #                                                                                                                  #
#                                                                                                                           #
#   #########################################################################################                               #
#                                                                                                                           #
#   # ffmpeg dnxhd encoder #                                                                                                #
#                                                                                                                           #
#   /Volumes/Agency-1/LT-Tools/_ffmpeg/ffmpeg -i /src/dir/ -vf format=yuv422p,scale=-1:1080,pad=1920:1080 -r 24000/1001     #
#   -c:v dnxhd -b:v 115M -c:a pcm_s16be /dst/dir/*;.mov                                                                     #
#                                                                                                                           #
#   #########################################################################################                               #
#                                                                                                                           #
#   # ffmpeg audio channels to stereo #                                                                                     #
#                                                                                                                           #
#   /Volumes/Agency-1/LT-Tools/_ffmpeg/ffmpeg -i "/input/dir" -af                                                           #
#   "pan=stereo|FL < 1.0*FL + 0.707*FC + 0.707*BL|FR < 1.0*FR + 0.707*FC + 0.707*BR" -c:v libx264 -preset medium            #
#   -tune fastdecode -vf scale=1920:-1 -pix_fmt yuv420p -movflags +faststart "/dst/dir"                                     #
#                                                                                                                           #
#   #########################################################################################                               #
#                                                                                                                           #
#   # directory copy #                                                                                                      #
#                                                                                                                           #
#   rsync -avP -f"+ */" -f"+ *.mov" -f"- *" "/src/dir" "/dst/dir"                                                           #
#                                                                                                                           #
#   #for windows directory copy#                                                                                            #
#   robocopy <Source> <Destination> *.mov /MIR                                                                              #
#############################################################################################################################

############ IMPORTED MODULES ############
import sys
import os
import shutil
import subprocess
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import uuid
from collections import OrderedDict
from datetime import datetime
from tkinter import *
from tkinter.ttk import *

from PIL import Image, ImageTk
from hurry.filesize import size, si

##########################################

################################################################### GUI LAYOUT + GLOBAL VALUES ###################################################################

root = Tk()
root.title("Lord And Thomas Universal Encoder - Copyright © 2018 FCB Chicago")
root.resizable(0, 0)
frame = Frame(root)  # create a frame to be able to attach the scrollbar
t = Text(frame, width=80, bg="black",
         fg="green")  # the Text widget - the size of the widget define the size of the window
t.pack(side="left", fill="both")
s = Scrollbar(frame)
s.pack(side="right", fill="y")
# link the text and scrollbar widgets
s.config(command=t.yview)
t.config(yscrollcommand=s.set)
frame.pack()
root.update_idletasks()
t.update_idletasks()
root.update()
progress = Frame()
progress.pack(fill=X)
progressLine = Progressbar(progress, orient=HORIZONTAL, length=550, mode='determinate', maximum=100)
progressLine.pack(pady=5)

vid_codec = ('.webm', '.WEBM', '.mov', '.MOV', '.mpg', '.MPG', '.mp2', '.MP2', '.mpeg',
             '.MPEG', '.mpe', '.MPE', '.mpv', '.MPV', '.ogg', '.OGG', '.mp4', '.MP4',
             '.m4p', '.M4P', '.m4v', '.M4V', '.mxf', '.MXF')  # video file extensions

file_size = {}  # dictionary containing the file sizes, before and after conversion.


# used in video and audio conv functions.

###################################################################################################################################################################

################################################################# USER INTERACTIVE GUI FUNCTIONS ##################################################################
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def remove_conv_file(path, files_tag):
    for root, dir, files in os.walk(path):
        for filename in files:
            if filename.endswith("{}.mov".format(files_tag)):
                file_path = root + os.sep + filename
                os.remove(file_path)


def if_conv_dir_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def filename_no_extention(filename):
    filename_no_extension = os.path.splitext(os.path.basename(filename))[0]
    return filename_no_extension


def open_dialog_box(message):
    root.update()
    t.update_idletasks()
    folder_path = tkinter.filedialog.askdirectory(title=message)
    result = folder_path.replace('/', '\\')
    root.title(message)
    root.update()
    t.update_idletasks()
    return result


def choose_output():
    tkinter.messagebox.showinfo("Information", "Choose Output Directory!")


def choose_input():
    tkinter.messagebox.showinfo("Information", "Choose Input Directory!")


def stop_playing_repeat():
    tkinter.messagebox.showinfo("Information",
                                "Here's a Hint: Hit 'Yes' to quit or choose a directory already ya Dumbo!")


def stop_playing4():
    tkinter.messagebox.showinfo("Information",
                                "Gotta Keep on Trying Right!?... Wrong! I'm starting to feel sorry for you now, and I'm just a Machine")


def stop_playing3():
    tkinter.messagebox.showinfo("Information", "Who're you kidding, just call for an early Retirement already.")


def stop_playing2():
    tkinter.messagebox.showinfo("Information", "Tsk Tsk Tsk... I've Lost RESPECT for you now! ")


def stop_playing1():
    tkinter.messagebox.showinfo("Information", "This isn't Funny anymore.. Get your LIFE together!")


def stop_playing():
    tkinter.messagebox.showinfo("Information", "STOP Goofing Around!!.. Typical HUMAN!")


def end_message_box():
    top = Toplevel(root)
    top.title("Lord And Thomas Universal Encoder - Copyright © 2018 - FCB Chicago")
    top.resizable(0, 0)

    C = Canvas(top, height=160, width=200, bg='black')
    pic_path = resource_path('dogthing_03.png')
    filename = Image.open(pic_path)

    photo = ImageTk.PhotoImage(filename)
    image = C.create_image(105, 94, anchor="center", image=photo)

    C.pack()

    Label(top, text="All Good To Go! Click OK to EXIT this application.",
          foreground="blue", font="Times 14 bold", wraplength=200).pack()
    B = tkinter.Button(top, font="Helvetica 15 bold", activeforeground="green", text="OK", foreground="red",
                       padx=30, pady=10,
                       relief=RAISED, width=16, height=2,
                       command=lambda: [root.destroy(), sys.exit()])  # destroys root after approx 3 seconds.
    B.pack()
    top.mainloop()


def connectionError():
    tkinter.messagebox.showerror("Connection Error",
                                 "Oops! FFMPEG connection not found. Make sure you are connected to the network, then Try Again.")


def directory_copying_cancellation():
    result = tkinter.messagebox.askquestion("Cancellation", "Are You Sure you want to exit?", icon='warning')
    t.update_idletasks()
    root.update()
    return result


class Encoder:

    # Warning message if user clicks on Cancel on Output File Dialog Box

    # When FFMPEG installation is not found.

    # Pops open a message window upon successful completion of this program

    # Funny messages whenever user clicks on 'no' on the ask question prompt, after hitting cancel when selecting a
    # directory

    # Notifying users on the type of directory to choose

    # Main window, where user selects an encoder.
    def __init__(self):
        self.converted_file_tag = self.unique_id()
        self.converted_dir_tag = self.unique_id()
        self.stepFiles_conv = 100.0
        self.stepFiles_copy = 100.0

    def type_encode(self):
        top = Toplevel(root)
        top.title("Lord And Thomas Universal Encoder - Copyright © 2018 - FCB Chicago")
        top.geometry("500x400")
        top.resizable(0, 0)
        C = Canvas(top, height=180, width=500, bg='black')
        pic_path = resource_path('res/dogthing_03.png')
        filename = Image.open(pic_path)

        photo = ImageTk.PhotoImage(filename)
        image = C.create_image(105, 94, anchor="center", image=photo)

        C.pack()

        Label(top,
              text="Want to see something Funny? Trying hitting 'cancel' when choosing an input or output directory, then hit 'No' on the prompt. I Dare You!",
              font="Times 12 italic", foreground="blue", wraplength=340).pack()

        Label(top, text="Please choose the type of Encoder you need.", foreground="green", font="Helvetica 14 bold",
              wraplength=400).pack()

        B1 = tkinter.Button(top, font="Helvetica 15 bold", activeforeground="green", text="MOV Encoder", padx=30,
                            pady=10,
                            relief=RAISED, width=16, height=2, command=lambda: [top.withdraw(), self.mov_encode()])
        B2 = tkinter.Button(top, font="Helvetica 15 bold", activeforeground="green", text="DNXHD Encoder", padx=30,
                            pady=10,
                            relief=RAISED, width=16, height=2, command=lambda: [top.withdraw(), self.dnxhd_encode()])

        B1.pack(side='left')
        B2.pack(side='right')
        top.mainloop()

    # Opens window dialog box asking to choose a directory.

    ###################################################################################################################################################################

    def multipleChannels_to_stereo(self):
        for subdir, dirs, files in os.walk(self.Input):  # accessing directory, sub-directories, and finally files
            for file in files:
                filepath = subdir + os.sep + file
                output_same_dirpath = subdir + os.sep
                if filepath.endswith("{}.mov".format(self.converted_file_tag)) and self.converted_dir_tag in filepath:
                    inpt = filepath  # filepaths only for files ending in unique tag id + .mov
                    no_extention = filename_no_extention(file)
                    file_no_extention = no_extention.replace(self.converted_file_tag, '')
                    output_same_dirpath = output_same_dirpath.replace('{}/'.format(self.converted_dir_tag), '')
                    outpt = output_same_dirpath + file_no_extention

                    stereo_code = ['.\\res\\ffmpeg\\bin\\ffmpeg.exe', '-i', '{}'.format(inpt), '-ac', '2',
                                   '-af', 'pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR', '-c:v', 'libx264',
                                   '-preset', 'medium', '-tune', 'fastdecode', '-vf', 'scale=1920:-1', '-pix_fmt',
                                   'yuv420p', '-movflags', '+faststart',
                                   '{}{}.mov'.format(outpt, self.converted_file_tag)]

                    if not os.path.exists(outpt + self.converted_file_tag + ".mov"):
                        try:
                            self.os_call_conv(stereo_code)
                        except OSError:  # exception to the error when ffmpeg directory is not found.
                            progressLine.update_idletasks()
                            connectionError()  # calls the gui function to display a connection dialog box.
                            root.destroy()
                            sys.exit()

    def mov_encode(self):
        count_goof = 0
        count_conv = 0
        count_copy = 0
        filecount_before = 1
        filecount_after = 1

        choose_input()
        self.Input = open_dialog_box("MOV Encoder - Copyright © 2018 FCB Chicago")

        if self.Input == '':
            while self.Input == '':
                result = directory_copying_cancellation()
                if result == 'yes':
                    end_message_box()
                else:
                    if count_goof == 0:
                        stop_playing()
                        count_goof += 1
                    elif count_goof == 1:
                        stop_playing1()
                        count_goof += 1
                    elif count_goof == 2:
                        stop_playing2()
                        count_goof += 1
                    elif count_goof == 3:
                        stop_playing3()
                        count_goof += 1
                    elif count_goof == 4:
                        stop_playing4()
                        count_goof += 1
                    else:
                        stop_playing_repeat()
                        count_goof += 1

        for a, b, f in os.walk(self.Input):
            for filenames in f:
                Path = a + os.sep + filenames
                if Path.endswith(vid_codec):
                    count_conv += 1
                if Path.endswith(vid_codec) and not Path.endswith("{}.mov".format(self.converted_file_tag)):
                    count_copy += 1

        if count_copy > 0:
            self.stepFiles_conv = (100.0 / count_conv)
            self.stepFiles_copy = (100.0 / count_copy)
            progressLine['value'] = 0
        else:
            self.stepFiles_conv = 100.0
            self.stepFiles_copy = 100.0

        for subdir, dirs, files in os.walk(self.Input):  # accessing directory, sub-directories, and finally files
            for file in files:
                filepath = subdir + os.sep + file
                output_same_dirpath = subdir + os.sep
                if filepath.endswith(vid_codec):  # only continue IF the current file is in specified format
                    input_filepath = filepath  # each specified format file from source directory
                    file_no_extention = filename_no_extention(file)
                    output_samedir = output_same_dirpath + self.converted_dir_tag + os.sep + file_no_extention  # each file (without specified format) added to the destination path

                    if_conv_dir_exists(output_same_dirpath + self.converted_dir_tag + os.sep)

                    if input_filepath.endswith(vid_codec) and not input_filepath.endswith(
                            "{}.mov".format(self.converted_file_tag)):
                        before_conv_path = input_filepath
                        before_byte_filesize = os.path.getsize(before_conv_path)
                        before_filesize = size(before_byte_filesize, system=si)
                        file_size['Data File Size {}'.format(filecount_before)] = []
                        file_size['Data File Size {}'.format(filecount_before)].append(before_filesize)
                        filecount_before += 1

                    progressLine.update_idletasks()
                    ffmpeg_code = ['.\\res\\ffmpeg\\bin\\ffmpeg.exe','-i',
                                   '{}'.format(input_filepath), '-vcodec', 'h264',
                                   '-acodec', 'mp2',
                                   '{}{}.mp4'.format(output_samedir, self.converted_file_tag)]

                    #ffmpeg_code = ['.\\res\\ffmpeg\\bin\\ffmpeg.exe','-i',
                     #              '{}'.format(input_filepath), '-map', '0', '-c',
                      #             'copy', '-c:v', 'libx264', '-preset', 'medium',
                       #            '-tune', 'fastdecode', '-vf', 'scale=1920:-1',
                        #           '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                         #          '{}{}.mov'.format(output_samedir, self.converted_file_tag)]

                    
                    if not os.path.exists(output_samedir + self.converted_file_tag + ".mov"):
                        try:
                            self.os_call_conv(ffmpeg_code)  # actual ffmpeg conversion takes place
                            #self.multipleChannels_to_stereo()
                            progressLine.step(self.stepFiles_conv)
                            progressLine.update_idletasks()
                            root.update_idletasks()
                        except OSError:  # exception to the error when ffmpeg directory is not found.
                            progressLine.update_idletasks()
                            connectionError()  # calls the gui function to display a connection dialog box.
                            root.destroy()
                            sys.exit()

            progressLine.update_idletasks()
        progressLine['value'] = 100
        progressLine.update_idletasks()

        src = self.Input
        choose_output()
        dst = open_dialog_box("MOV Encoder - Copyright © 2018 FCB Chicago")

        count_goof = 0

        if dst == '':
            while dst == '':
                result = directory_copying_cancellation()
                if result == 'yes':
                    end_message_box()
                else:
                    if count_goof == 0:
                        stop_playing()
                        count_goof += 1
                    elif count_goof == 1:
                        stop_playing1()
                        count_goof += 1
                    elif count_goof == 2:
                        stop_playing2()
                        count_goof += 1
                    elif count_goof == 3:
                        stop_playing3()
                        count_goof += 1
                    elif count_goof == 4:
                        stop_playing4()
                        count_goof += 1
                    else:
                        stop_playing_repeat()
                        count_goof += 1
                    dst = open_dialog_box("MOV Encoder - Copyright © 2018 FCB Chicago")

        progressLine['value'] = 0
        progressLine.update_idletasks()

        self.remove_conv_dir(src)

        count_mov = 1
        if os.path.exists(dst + '/' + 'MOV_Encoder_{}'.format(count_mov)):
            while os.path.exists(dst + '/' + 'MOV_Encoder_{}'.format(count_mov)):
                count_mov += 1

        copy_code = 'rsync -avP -f"+ */" -f"+ *{}.mov" -f"- *" "{}" "{}/MOV_Encoder_{}"'.format(self.converted_file_tag,
                                                                                                src, dst, count_mov)

        try:
            self.os_call_copy(copy_code)  # copying directory structure to destination folder.
        except OSError:  # exception to the error when ffmpeg directory is not found.
            progressLine.update_idletasks()
            connectionError()  # calls the gui function to display a connection dialog box.
            root.destroy()
            sys.exit()

        progressLine.update_idletasks()
        t.update_idletasks()
        root.update()
        self.renaming(dst, self.converted_file_tag)  # renaming moved files back to their original names.

        if dst != '':
            for a, b, c in os.walk(dst + "/MOV_Encoder_{}".format(count_mov)):
                for conv_files in c:
                    conv_path = a + os.sep + conv_files
                    if conv_path.endswith(
                            ".mov") and "DNXHD_Encoder" not in conv_path and self.converted_dir_tag not in conv_path:
                        try:
                            after_conv_path = conv_path
                            after_byte_filesize = os.path.getsize(after_conv_path)
                            after_filesize = size(after_byte_filesize, system=si)
                            file_size['Data File Size {}'.format(filecount_after)].append(after_filesize)
                            filecount_after += 1
                        except OSError:  # exception to the error when ffmpeg directory is not found.
                            progressLine.update_idletasks()
                            connectionError()  # calls the gui function to display a connection dialog box.
                            root.destroy()
                            sys.exit()

        t.tag_config("documentation", foreground="white")
        end_time = datetime.now()
        time_duration = '#### MOV Encoding Time: {} ####'.format(end_time - start_time)
        t.insert(END, "\n")
        t.insert(END, "\n")
        t.insert(END, time_duration, "documentation")

        try:
            t.see(END)
            t.update_idletasks()
        except OSError:  # exception to the error when ffmpeg directory is not found.
            progressLine.update_idletasks()
            connectionError()  # calls the gui function to display a connection dialog box.
            root.destroy()
            sys.exit()

        # ordered dictionary
        file_size_ordered = OrderedDict((k, v) for k, v in sorted(list(file_size.items()), key=lambda x: x[0]))

        # Parsing through the dictionary used for storing file sizes (before and after conversion)
        try:
            for i in file_size_ordered:
                t.insert(END, "\n")
                t.insert(END, "\n")
                t.insert(END, "\n")
                t.insert(END, "#### {} ####".format(i), "documentation")
                t.insert(END, "\n")
                t.insert(END, "\n")
                t.insert(END, "Before Conversion: {}".format(file_size_ordered[i][0]), "documentation")
                t.insert(END, "\n")
                t.insert(END, "After Conversion: {}".format(file_size_ordered[i][1]), "documentation")
                t.see(END)
                t.update_idletasks()
        except OSError:  # exception to the error when ffmpeg directory is not found.
            progressLine.update_idletasks()
            connectionError()  # calls the gui function to display a connection dialog box.
            root.destroy()
            sys.exit()

        t.insert(END, "\n")
        t.insert(END, "\n")
        t.see(END)
        t.update_idletasks()

        remove_conv_file(self.Input, self.converted_file_tag)  # remove temporary conversion files at the end

        end_message_box()  # display completion.

    def dnxhd_encode(self):
        count_goof = 0
        count_conv = 0
        count_copy = 0
        filecount_before = 1
        filecount_after = 1
        tag_file = self.unique_id()

        choose_input()
        self.Input = open_dialog_box("DNXHD Encoder - Copyright © 2018 FCB Chicago")

        if self.Input == '':
            while self.Input == '':
                result = directory_copying_cancellation()
                if result == 'yes':
                    end_message_box()
                else:
                    if count_goof == 0:
                        stop_playing()
                        count_goof += 1
                    elif count_goof == 1:
                        stop_playing1()
                        count_goof += 1
                    elif count_goof == 2:
                        stop_playing2()
                        count_goof += 1
                    elif count_goof == 3:
                        stop_playing3()
                        count_goof += 1
                    elif count_goof == 4:
                        stop_playing4()
                        count_goof += 1
                    else:
                        stop_playing_repeat()
                        count_goof += 1
                    self.Input = open_dialog_box("DNXHD Encoder - Copyright © 2018 FCB Chicago")

        for a, b, f in os.walk(self.Input):
            for filenames in f:
                Path = a + os.sep + filenames
                if Path.endswith(vid_codec):
                    count_conv += 1
                if Path.endswith(vid_codec) and not Path.endswith("{}.mov".format(tag_file)):
                    count_copy += 1

        if count_copy > 0:
            self.stepFiles_conv = (100.0 / count_conv)
            self.stepFiles_copy = (100.0 / count_copy)
            progressLine['value'] = 0
        else:
            pass

        for subdir, dirs, files in os.walk(self.Input):  # accessing directory, sub-directories, and finally files
            for file in files:
                filepath = subdir + os.sep + file
                output_same_dirpath = subdir + os.sep
                if filepath.endswith(vid_codec):  # only continue IF the current file is in specified format
                    input_filepath = filepath  # each specified format file from source directory
                    file_no_extention = filename_no_extention(file)
                    output_samedir = output_same_dirpath + file_no_extention  # each file (without extention) added
                    # to the destination path

                    if input_filepath.endswith(vid_codec) and not input_filepath.endswith("{}.mov".format(tag_file)):
                        before_conv_path = input_filepath
                        before_byte_filesize = os.path.getsize(before_conv_path)
                        before_filesize = size(before_byte_filesize, system=si)
                        file_size['Data File Size {}'.format(filecount_before)] = []
                        file_size['Data File Size {}'.format(filecount_before)].append(before_filesize)
                        filecount_before += 1

                    progressLine.update_idletasks()

                    ffmpeg_code = ['.\\res\\ffmpeg\\bin\\ffmpeg.exe','-i', '{}'.format(input_filepath),
                                   '-vf', 'format=yuv422p,scale=-1:1080,pad=1920:1080', '-r', '24000/1001',
                                   '-c:v', 'dnxhd', '-b:v', '115M', '-c:a', 'pcm_s16be',
                                   '{}{}.mov'.format(output_samedir, tag_file)]

                    if not os.path.exists(output_samedir + tag_file + ".mov"):
                        try:
                            self.os_call_conv(ffmpeg_code)  # ffmpeg bash call.
                            progressLine.step(self.stepFiles_conv)
                            progressLine.update_idletasks()
                            root.update_idletasks()
                        except OSError:  # exception to the error when ffmpeg directory is not found.
                            progressLine.update_idletasks()
                            connectionError()  # connection error call.
                            root.destroy()
                            sys.exit()

            progressLine.update_idletasks()
        progressLine['value'] = 100
        progressLine.update_idletasks()

        src = self.Input
        choose_output()
        dst = open_dialog_box("DNXHD Encoder - Copyright © 2018 FCB Chicago")

        count_goof = 0

        if dst == '':
            while dst == '':
                result = directory_copying_cancellation()
                if result == 'yes':
                    end_message_box()
                else:
                    if count_goof == 0:
                        stop_playing()
                        count_goof += 1
                    elif count_goof == 1:
                        stop_playing1()
                        count_goof += 1
                    elif count_goof == 2:
                        stop_playing2()
                        count_goof += 1
                    elif count_goof == 3:
                        stop_playing3()
                        count_goof += 1
                    elif count_goof == 4:
                        stop_playing4()
                        count_goof += 1
                    else:
                        stop_playing_repeat()
                        count_goof += 1
                    dst = open_dialog_box("DNXHD Encoder - Copyright © 2018 FCB Chicago")

        progressLine['value'] = 0
        progressLine.update_idletasks()

        count_dnxhd = 1
        if os.path.exists(dst + '/' + 'DNXHD_Encoder_{}'.format(count_dnxhd)):
            while os.path.exists(dst + '/' + 'DNXHD_Encoder_{}'.format(count_dnxhd)):
                count_dnxhd += 1

        copy_code = 'rsync -avP -f"+ */" -f"+ *{}.mov" -f"- *" "{}" "{}/DNXHD_Encoder_{}"'.format(tag_file, src, dst,
                                                                                                  count_dnxhd)

        try:
            self.os_call_copy(copy_code)  # copying directory structure to destination folder.
        except OSError:  # exception to the error when ffmpeg directory is not found.
            progressLine.update_idletasks()
            connectionError()  # calls the gui function to display a connection dialog box.
            root.destroy()
            sys.exit()

        progressLine.update_idletasks()
        t.update_idletasks()
        root.update()
        self.renaming(dst, tag_file)  # renaming moved files back to their original names.

        if dst != '':
            for a, b, c in os.walk(dst + "/DNXHD_Encoder_{}".format(count_dnxhd)):
                for conv_files in c:
                    conv_path = a + os.sep + conv_files
                    if conv_path.endswith(".mov") and "MOV_Encoder" not in conv_path:
                        try:
                            after_conv_path = conv_path
                            after_byte_filesize = os.path.getsize(after_conv_path)
                            after_filesize = size(after_byte_filesize, system=si)
                            file_size['Data File Size {}'.format(filecount_after)].append(after_filesize)
                            filecount_after += 1
                        except OSError:  # exception to the error when ffmpeg directory is not found.
                            progressLine.update_idletasks()
                            connectionError()  # calls the gui function to display a connection dialog box.
                            root.destroy()
                            sys.exit()

        t.tag_config("documentation", foreground="white")
        end_time = datetime.now()
        time_duration = '#### DNXHD Encoding Time: {} ####'.format(end_time - start_time)
        t.insert(END, "\n")
        t.insert(END, "\n")
        t.insert(END, time_duration, "documentation")
        try:
            t.see(END)
            t.update_idletasks()
        except OSError:  # exception to the error when ffmpeg directory is not found.
            progressLine.update_idletasks()
            connectionError()  # calls the gui function to display a connection dialog box.
            root.destroy()
            sys.exit()

        # ordered dictionary
        file_size_ordered = OrderedDict((k, v) for k, v in sorted(list(file_size.items()), key=lambda x: x[0]))

        try:
            for i in file_size_ordered:
                t.insert(END, "\n")
                t.insert(END, "\n")
                t.insert(END, "\n")
                t.insert(END, "#### {} ####".format(i), "documentation")
                t.insert(END, "\n")
                t.insert(END, "\n")
                t.insert(END, "Before Conversion: {}".format(file_size_ordered[i][0]), "documentation")
                t.insert(END, "\n")
                t.insert(END, "After Conversion: {}".format(file_size_ordered[i][1]), "documentation")
                t.see(END)
                t.update_idletasks()
        except OSError:  # exception to the error when ffmpeg directory is not found.
            progressLine.update_idletasks()
            connectionError()  # calls the gui function to display a connection dialog box.
            root.destroy()
            sys.exit()

        t.insert(END, "\n")
        t.insert(END, "\n")
        t.see(END)
        t.update_idletasks()

        remove_conv_file(self.Input, tag_file)  # remove temporary conversion files at the end

        end_message_box()  # display completion.

    # Removes extension from the filename

    # Creates temporary directory storage for converted .mov files(if not already created), 
    # before multipleChannels_to_stereo function takes place. 

    # Removes temporary directory storage for converted .mov files
    def remove_conv_dir(self, path):
        for root, dir, files in os.walk(path):
            for dirname in dir:
                if dirname == self.converted_dir_tag:
                    dirpath = root + os.sep + dirname
                    shutil.rmtree(dirpath)

    # Removes temporary converted files with unique id

    # Generating unique random names for temporary files or folders.
    @staticmethod
    def unique_id():
        tags = uuid.uuid4().hex
        return tags

    # Renames the temporary named converted file (while the copying process) back its original name.
    @staticmethod
    def renaming(path, file_tag):
        for subdir, dirs, files in os.walk(path):  # accessing directory, sub-directories, and finally files
            for filename in files:
                if filename.endswith("{}.mov".format(file_tag)):
                    old_path = subdir + os.sep + filename
                    new_name = filename.replace(file_tag, '')
                    new_path = subdir + os.sep + new_name
                    os.renames(old_path, new_path)

    # For ffmpeg running in bash (takes in a list as an argument)
    def os_call_conv(self, command):
        process = subprocess.Popen(args=command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print((output.strip()))
                t.insert(END, output)
                t.see(END)
                t.update_idletasks()
                root.update()
        rc = process.poll()
        return rc

    # For the directory structure copying running in bash (takes in a string as an argument)
    def os_call_copy(self, command):
        process = subprocess.Popen(args=command, executable='bash', stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                progressLine.step(self.stepFiles_copy)
                progressLine.update_idletasks()
                t.insert(END, output)
                t.see(END)
                t.update_idletasks()
                root.update()
                print((output.strip()))
        rc = process.poll()
        progressLine['value'] = 100
        progressLine.update_idletasks()
        return rc

start_time = datetime.now()
encoder = Encoder()
encoder.type_encode()  # calling the entire python program
