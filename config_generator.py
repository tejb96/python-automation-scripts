import yaml
import os
import sys
import platform
from tkinter import *
from PIL import Image, ImageTk


def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")  # Adjust for Linux, getting current directory

    return os.path.join(basePath, relativePath)


def ensure_dir():
    directory = os.path.dirname('config')
    print(directory)
    if not os.path.exists('config'):
        os.makedirs('config')


# Check for the config file
bool_config = os.path.isfile(resourcePath('pybot-config.yaml'))

if not bool_config:
    f = open(resourcePath("pybot-config.yaml"), "w")
    config_list = [['client title', 'OpenOSRS'], ['pc_profile', '/home/username/OpenOSRS_profile'],
                   ['file_path_to_client', '/.openosrs/'], ['tesseract_path', '/usr/bin/tesseract'],
                   ['enable_on_start', True]]

    article_info = [{
        'Config': {
            'client_title': config_list[0][1],
            'pc_profile': config_list[1][1],
            'file_path_to_client': config_list[2][1],
            'tesseract_path': config_list[3][1],
            'enable_on_start': config_list[4][1]
        }
    }]
    yaml.dump(article_info, f)
    f.close()

bool_config = os.path.isfile(resourcePath('pybot-config.yaml'))
if bool_config:
    print('config already exists!')
    with open(resourcePath("pybot-config.yaml"), "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print("Read successful")
    print(data)

    config_list = [['client title', data[0]['Config']['client_title']],
                   ['pc_profile', data[0]['Config']['pc_profile']],
                   ['file_path_to_client', data[0]['Config']['file_path_to_client']],
                   ['tesseract_path', data[0]['Config']['tesseract_path']],
                   ['enable_on_start', data[0]['Config']['enable_on_start']]
                   ]
ensure_dir()

if data[0]['Config']['enable_on_start'] == True:
    root = Tk()
    root.title('Sly OSRS PyBot_Config')
    root.geometry('715x465')
    root.configure(background='#40362C')

    Font_tuple = ('Unispace', 15)  # You may need to install the Unispace font or use a common font
    Font_tuple_entry = ('Unispace', 10)
    filename = resourcePath('images/osrs_title_2.png')
    image1 = Image.open(filename)
    image1 = image1.convert('RGBA')
    image1.thumbnail((400, 400))
    test1 = ImageTk.PhotoImage(image1)
    label1 = Label(image=test1, background='#40362C', anchor=CENTER, justify=CENTER)
    label1.image = test1
    label1.grid(column=0, columnspan=2)

    x = 1
    while x < len(config_list) + 1:
        lbl = Label(root, text=(config_list[(x - 1)][0]), background='#40362C', fg='yellow', padx=20)
        lbl.configure(font=Font_tuple)
        lbl.grid(column=0, row=x)
        x += 1

    x = 1
    test = []
    while x < len(config_list) + 1:
        if config_list[(x - 1)][0] != 'enable_on_start':
            txt = Entry(root, width=50, background='#40362C', fg='yellow')
            txt.insert(-1, (config_list[(x - 1)][1]))
            txt.configure(font=Font_tuple_entry)
            test.append(txt)
            txt.grid(column=1, row=x)
        x += 1

    is_on = True
    image1 = Image.open(resourcePath('images/switch-on.png'))
    image1 = image1.convert('RGBA')
    image1.thumbnail((50, 50))
    on = ImageTk.PhotoImage(image1)
    image2 = Image.open(resourcePath('images/switch-off.png'))
    image2 = image2.convert('RGBA')
    image2.thumbnail((50, 50))
    off = ImageTk.PhotoImage(image2)


    def toggle():
        global is_on
        if is_on:
            toggle_btn.config(image=off)
            is_on = False
        else:
            toggle_btn.config(image=on)
            is_on = True


    toggle_btn = Button(image=on, width=50, background='#40362C', activebackground='#40362C', bd=0, relief=None,
                        fg='yellow', command=toggle)
    toggle_btn.grid(column=0, row=5, columnspan=2, pady=2)


    def clicked():
        c_title = test[0].get()
        t_enable = is_on
        p_profile = test[1].get()
        f_path = test[2].get()
        t_path = test[3].get()
        article_info = [
            {
                'Config': {
                    'client_title': c_title,
                    'pc_profile': p_profile,
                    'file_path_to_client': f_path,
                    'tesseract_path': t_path,
                    'enable_on_start': t_enable
                }
            }
        ]
        with open("pybot-config.yaml", 'w') as yamlfile:
            yaml.dump(article_info, yamlfile)
            print("Write successful")

        with open("pybot-config.yaml", "r") as yamlfile:
            data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            print("Read successful")
        print(data)
        root.quit()
        root.destroy()


    btn = Button(root, text='Generate Config File', fg='yellow', command=clicked, background='#40362C', pady=0)
    btn.grid(column=0, row=6, columnspan=2, pady=2)
    btn.configure(font=Font_tuple)
    root.mainloop()
