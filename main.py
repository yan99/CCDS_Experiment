import random
import os
import glob
import pickle
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import math
import numpy as np

class Evaluate(tk.Tk):

    def __init__(self, pathone, pathtwo, paththree):
        self.score_list = []
        self.dict = {}
        page_size = len(pathone)
        self.pages = [num for num in range(page_size)]

        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "--Content-Color-Dependent Screening Halftone Subjective Assessment --")

        container = tk.Frame(self)
        container.pack(side="top", fill='both', expand=True)
        # container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for idx in self.pages:
            frame = OnePage(idx, pathone, pathtwo, paththree, page_size, self.dict, container, self)
            frame.grid(row=0, column=0, sticky="nsew")
#            self.dict[idx] = frame.missChecking_dict[page_size-1-idx]
#            print('Hello\n')
            self.frames[idx] = frame

    def show_frame(self, num):
        frame = self.frames[num]
        frame.tkraise()

    def write(self):
        length = len(self.frames)

        for idx in range(length):
            name1 = self.frames[idx].name_red
            name2 = self.frames[idx].name_yel
            score1 = self.frames[idx].v_red.get()
            misschecking = self.frames[idx].missChecking_dict
#            print(misschecking)
#            print(self.dict)
#            score2 = self.frames[idx].v_red.get()
            self.score_list.append((name1, name2, score1))
#            self.score_list.append((name2, score2))

class OnePage(tk.Frame):

    def __init__(self, idx, pathone, pathtwo, paththree, size, dict_, parent, controller):
        tk.Frame.__init__(self, parent)

        self.missChecking_dict = dict_
        self.size = size
        self.controller = controller
        screen_height = 0.8 * controller.winfo_screenheight() 
        screen_width = 0.9 * controller.winfo_screenwidth() 
#        ratio = screen_height * screen_width * (0.2 / (1728 * 864))
        ratio = 1
#        print(ratio)

        if idx == 0:
            status = tk.Label(self, text = 'Image ' + str(size-idx)+ ' / ' + str(size), bd = 1, anchor = 'e')
            status.pack(side='bottom', fill='x', padx=10, pady=2)       
            
            
            finish = tk.Button(self, text='Done', command=self.dest)
#            finish.pack(side='bottom', fill='x', padx=ratio*screen_width * 800 / 1728, pady=2)
            finish.pack(side='bottom', fill='x', padx=1, pady=2)

            prev = tk.Button(self, text='Prev', command=(lambda: controller.show_frame(idx + 1)))
            prev.pack(side='bottom', fill='x', padx=1, pady=2)

            label = tk.Label(self, text='IMPORTANT!!! \n Please click on "Done" \n to save and exit. \n Thank you for participating!')
            label.config(font=('helvetica', 12), bg='green', fg='black', width=30, height=5)
            label.pack(side='bottom', padx=10, pady=10)


        if idx < (size - 1) and idx > 0:
            status = tk.Label(self, text = 'Image ' + str(size-idx)+ ' / ' + str(size), bd = 1, anchor = 'e')
            status.pack(side='bottom', fill='x', padx=10, pady=2)
            
            go = tk.Button(self, text='Next', command=(lambda: controller.show_frame(idx - 1)))
            go.pack(side='bottom', fill='x', padx=1, pady=2)

            prev = tk.Button(self, text='Prev', command=(lambda: controller.show_frame(idx + 1)))
            prev.pack(side='bottom', fill='x', padx=1, pady=2)

        if idx == (size - 1):
            status = tk.Label(self, text = 'Image ' + str(size-idx)+ ' / ' + str(size), bd = 1, anchor = 'e')
            status.pack(side='bottom', fill='x', padx=10, pady=2)
            go = tk.Button(self, text='Next', command=(lambda: controller.show_frame(idx - 1)))
            go.pack(side='bottom', fill='x', padx=1, pady=2)


        word = "Contact: yan99@purdue.edu\n"
        label = tk.Label(self, text=word, bg='grey', fg='black', padx= 15, pady=5)
        label.config(font=('helvetica', 10))
        label.pack(side='top', padx=5, pady=10)

        red_bar = tk.LabelFrame(self, text=" LEFT IMAGE ", padx=9, pady=5)
        red_bar.pack(side='left', padx=10, pady=10)
        
        yellow_bar = tk.LabelFrame(self, text=" RIGHT IMAGE ", padx=9, pady=5)
        yellow_bar.pack(side='right', padx=10, pady=10)        

        LANGS = [('Left image better', 1), ('Right image better', 2)]
        self.v_red = tk.IntVar()
        self.v_red.set(0)
        for long, num in LANGS:
            if num == 1:
                b = tk.Radiobutton(red_bar, text=long, variable=self.v_red, value=num, command = lambda: self.clicked(idx,self.v_red.get()))
                b.pack(anchor='w')
            elif num == 2:
                b = tk.Radiobutton(yellow_bar, text=long, variable=self.v_red, value=num, command = lambda: self.clicked(idx,self.v_red.get()))
                b.pack(anchor='w')                
        
#        print(self.v_red)
#        if self.v_red.get()== 0:
##            print('1\n')
#            self.missChecking_dict[idx] = 0
#        else:
##            print('2\n')
#            self.missChecking_dict[idx] = 1
            
#        yellow_bar = tk.LabelFrame(self, text=" RIGHT IMAGE ", padx=9, pady=5)
#        yellow_bar.pack(side='right', padx=10, pady=10)

#        self.v_yel = tk.IntVar()
#        self.v_yel.set(0)
#        for long, num in LANGS:
#            b = tk.Radiobutton(yellow_bar, text=long, variable=self.v_yel, value=num)
#            b.pack(anchor='w')

        vbar1 = tk.Scrollbar(self, orient='vertical')
        vbar1.pack(side='left', fill='y')

        vbar2 = tk.Scrollbar(self, orient='vertical')
        vbar2.pack(side='right', fill='y')

        hbar = tk.Scrollbar(self, orient='horizontal')
        hbar.pack(side='bottom', fill='x')

#        print(pathone[idx])
        img_name_red = os.path.split(pathone[idx])[1]
#        print(img_name_red)
        img_name_red = img_name_red.split('.')
#        print(img_name_red)
        img_name_red = img_name_red[0]
#        print(img_name_red)
        self.name_red = img_name_red

        img_name_yel = os.path.split(pathtwo[idx])[1]
        img_name_yel = img_name_yel.split('.')
        img_name_yel = img_name_yel[0]
        self.name_yel = img_name_yel

        image1 = Image.open(pathone[idx])
        old_width1, old_height1 = image1.size
        # ratio1 = screen_height/old_height1 * 0.9
        ratio1 = ratio
#        ratio1 = 0.8
        new_width1, new_height1 = int(old_width1 * ratio1), int(old_height1 * ratio1)
        image1 = image1.resize((new_width1, new_height1), Image.ANTIALIAS)
        photo1 = ImageTk.PhotoImage(image1, master=self)

        image2 = Image.open(pathtwo[idx])
        old_width2, old_height2 = image2.size
        new_width2, new_height2 = int(old_width2 * ratio1), int(old_height2 * ratio1)
        image2 = image2.resize((new_width2, new_height2), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(image2, master=self)

        self.canvas1 = tk.Canvas(self, bd=0, highlightthickness=2, highlightbackground="black", relief='ridge',xscrollcommand = hbar.set, yscrollcommand=vbar1.set, scrollregion=(-200, -200, new_width2+200, new_height2+100))

        y0 = (self.canvas1.winfo_screenheight() - 200 )/4
        x0 = (self.canvas1.winfo_screenwidth() - 200 )/4

        self.canvas1.create_image((x0,y0), anchor='center', image=photo1)
        self.canvas1.image = photo1
        self.canvas1.pack(side='left', fill='both', expand=True)
        # self.canvas1.place(relx=0.5, rely=0.5, anchor='center')
        vbar1.config(command=lambda *args: self.yviewall(*args))
        self.canvas1.config(yscrollcommand=vbar1.set)
        # hbar1.config(command=canvas1.xview)
        # canvas1.config(xscrollcommand=hbar1.set)

        self.canvas2 = tk.Canvas(self, bd=0, highlightthickness=2, highlightbackground="black", relief='ridge', xscrollcommand = hbar.set, yscrollcommand=vbar2.set, scrollregion=(-200, -200, new_width2+200, new_height2+100))

        self.canvas2.create_image((x0,y0), anchor='center', image=photo2)
        self.canvas2.image = photo2
        self.canvas2.pack(side='right', fill='both', expand=True)
        # vbar2.config(command=self.canvas2.yview)
        vbar2.config(command=lambda *args: self.yviewall(*args))
        # canvas2.config(yscrollcommand=vbar2.set)
        # canvas2.config(yscrollcommand=vbar2.set)
        hbar.config(command=lambda *args: self.xviewall(*args))
        # canvas2.config(xscrollcommand=hbar2.set)


        image3 = Image.open(paththree[idx])
        old_width3, old_height3 = image3.size
        image3 = image3.resize((int(screen_width*0.20), int(screen_width*0.20*old_height3/old_width3)), Image.ANTIALIAS)
        photo_ref = ImageTk.PhotoImage(image3, master=self)

        self.canvas3 = tk.Canvas(self, bd=0, highlightthickness=1, highlightbackground="black", relief='ridge')

        self.canvas3.create_image((image3.size[0]//2,image3.size[1]//2), anchor='center', image=photo_ref)
        self.canvas3.image = photo_ref
        self.canvas3.pack(side='top', fill = 'both',expand=True)
        # vbar2.config(command=self.canvas2.yview)
        # canvas2.config(yscrollcommand=vbar2.set)
        # canvas2.config(yscrollcommand=vbar2.set)
        # canvas2.config(xscrollcommand=hbar2.set)


    def xviewall(self, *args):
        self.canvas1.xview(*args)
        self.canvas2.xview(*args)

    def yviewall(self, *args):
        self.canvas1.yview(*args)
        self.canvas2.yview(*args)

    
    def dest(self):
        cnt = 0
        out_str = ""
        for idx in range(self.size):
            if not idx in self.missChecking_dict:
                cnt+=1
                out_str += str(self.size-idx) + ',' + ' '
            
        if cnt!=0:
            messagebox.showwarning("Warning","Sorry, You missed to click image"+out_str)
#            print(self.missChecking_dict)
        else:
            self.controller.write()
            self.destroy()
            self.controller.destroy()
    def clicked(self,idx, value):
        self.missChecking_dict[idx] = value

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
glob_one = os.path.join(PROJECT_ROOT, 'algo1_zoom', '*.PNG')
glob_two = os.path.join(PROJECT_ROOT, 'algo2_zoom', '*.PNG')
glob_three = os.path.join(PROJECT_ROOT,'locate','*.jpg')
#glob_one = os.path.join(PROJECT_ROOT, 'algo1_test', '*.png')
#glob_two = os.path.join(PROJECT_ROOT, 'algo2_test', '*.png')
images_one = glob.glob(glob_one)
images_two = glob.glob(glob_two)
images_three = glob.glob(glob_three)

if len(images_one) == 0:
    raise ValueError("No images found in algo1 folder")
images_one.sort()

if len(images_two) == 0:
    raise ValueError("No images found in algo2 folder")
images_two.sort()

if len(images_three) == 0:
    raise ValueError("No images found in locate folder")
images_two.sort()

if (len(images_one) != len(images_two)) or (len(images_one) != len(images_three)) or (len(images_three) != len(images_two)):
    raise ValueError("Images mismatch")

print('\n\t\t Loading......\n')

zip_list = list(zip(images_one, images_two, images_three))


unchange_images1 = images_one
unchange_images2 = images_two
unchange_images3 = images_three
exchange_images1, exchange_images2, exchange_images3 = [], [],[]

n = len(images_one)

for num in range(math.floor(n/2)):
    temp1, temp2, temp3 = random.choice(zip_list)
    # repeat_images1.append(temp1)
    # repeat_images2.append(temp2)
    exchange_images3.append(temp3)
    exchange_images1.append(temp2)
    exchange_images2.append(temp1)

    unchange_images1.remove(temp1)
    unchange_images2.remove(temp2)
    unchange_images3.remove(temp3)
    zip_list = list(zip(unchange_images1, unchange_images2, unchange_images3))
    
pool_name1 = unchange_images1 + exchange_images1
pool_name2 = unchange_images2 + exchange_images2
pool_name3 = unchange_images3 + exchange_images3 
zip_list = list(zip(pool_name1, pool_name2, pool_name3))  
repeat_images1, repeat_images2, repeat_images3 = [], [], []
    
for num in range(math.floor(n/6)):
    temp1, temp2, temp3 = random.choice(zip_list)
    repeat_images1.append(temp1)
    repeat_images2.append(temp2)
    repeat_images3.append(temp3)


pool_name1_wrepeat = pool_name1 + repeat_images1
pool_name2_wrepeat = pool_name2 + repeat_images2
pool_name3_wrepeat = pool_name3 + repeat_images3
#pool_name1 = images_one
#pool_name2 = images_two    

zip_list2 = list(zip(pool_name1_wrepeat, pool_name2_wrepeat, pool_name3_wrepeat))
random.shuffle(zip_list2)
random.shuffle(zip_list2)

final_name1, final_name2, final_name3 = zip(*zip_list2)


print('\n\t\t GUI window loaded. \n\t\t If the Python window prompt does not appear, please open it manually. \n')
app = Evaluate(final_name1, final_name2, final_name3)
screen_height = app.winfo_screenheight()
screen_width = app.winfo_screenwidth()

win_width = 0.9 * screen_width
win_height = 0.8 * screen_height

show_width = (screen_width - win_width) / 2
show_height = (screen_height - win_height) / 2
app.geometry("%dx%d+%d+%d" % (win_width, win_height, show_width, show_height))

app.mainloop()

score = app.score_list

score_dict = {}
for (key1,key2, value) in score:
    if value == 1:
        image_name = key1.split('_')[1]
        algo_name = key1.split('_')[0]
        score_dict.setdefault(image_name, []).append(algo_name)
    elif value == 2:
        image_name = key2.split('_')[1]
        algo_name = key2.split('_')[0]        
        score_dict.setdefault(image_name, []).append(algo_name)
    else:
        image_name = key1.split('_')[1]
        score_dict.setdefault(image_name, []).append('0')

fn2 = os.path.join(PROJECT_ROOT, 'tempfile_part1.txt')
with open(fn2, 'w') as data:
    data.write(str(score_dict))
#
#if 0 in [x for v in score_dict.values() for x in v]:
#    print('\n\t\t You skipped some of the images. Scores are not recorded. Please restart.\n')
#    # print(score_dict)
#else:
print('\n\t\t Please email "tempfile_part1.txt" and "yourname_results_part1.txt" to \n\t\t yan99@purdue.edu \n\t\t Thank you for your time!')
print(score_dict)
fn = os.path.join(PROJECT_ROOT, 'yourname_results_part1.txt')
with open(fn, 'wb') as handle:
    pickle.dump(score_dict, handle)


