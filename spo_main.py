# -*- coding: utf-8 -*-
"""
Created on  2022-04-10

@author: ziyuan
@email:1104009634@qq.com
"""

import PySimpleGUI as sg
import re
import zhon.hanzi


# 功能部分
"""
# 读取txt文件
# 参数说明：
# txtPath：txt文件所在的路径
# return：分句后的结果
"""
def readtxt(txtPath):
    f=open(txtPath, encoding='utf-8')
    #f=open(txtPath)
    txt=[]
    for line in f:
        for sent in re.findall(zhon.hanzi.sentence, line):
            txt.append(sent)
    return txt

# GUI部分
sg.change_look_and_feel("GreenTan")


Left_list_column = [
     [
        sg.Text("请选择txt文件所在的目录：",font=("微软雅黑", 12)),
        sg.In(size=(30, 1), enable_events=True, key="-txt-"),
        sg.FileBrowse('浏览'),
        sg.Button('确定', enable_events=True, key="-confirm-"),
    ], 
    [   sg.Text("读取结果为：",font=("微软雅黑", 15))     ],
    [   sg.Listbox(values="", size=(90, 24), key='-multi-',horizontal_scroll=True,font=("宋体")) ], 
    [   sg.Text("请依次输入三元组(SPO)，点击next后存入",font=("微软雅黑", 12)) ], 
    [
        sg.Text("subject："),
        sg.In(size=(10, 1), enable_events=True, key="-subject-"),
        sg.Text("  predicate："),
        sg.In(size=(10, 1), enable_events=True, key="-predicate-"),
        sg.Text("  object："),
        sg.In(size=(10, 1), enable_events=True, key="-object-"),
        sg.Text("  "),
        sg.Button('next', enable_events=True, key="-next-"),
        sg.Text("", size=(20, 1), key="-TOUT-")
    ] 
]



Right_list_column = [
    [sg.Text("语义标注结果：",font=("微软雅黑", 12))],
    [sg.Listbox(values="", size=(30, 25), key="-result-",font=("宋体",15))],
    [sg.Text("请选择保存目录：",font=("微软雅黑", 12))],
    [   
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse('select'),
    ],
    [sg.Button('save', enable_events=True, key="-save-")],
]

layout =[
     [
     sg.Column(Left_list_column),
     sg.VSeperator(),
     sg.Column(Right_list_column),
 ]
]# end layout
window = sg.Window('语义三元组标注工具', layout)
while True:
    event, values = window.read()
    if event in (None,):
        break  # 相当于关闭界面
    elif event == "-confirm-":
        if values["-txt-"]:
            txt_list = readtxt(values["-txt-"])
            window["-multi-"].update(txt_list)
            #print(txt_list)
            tri_list = []
        else:
            sg.popup('请选择txt文件！！！')
    elif event == "-next-":
        subject = values["-subject-"]
        window["-subject-"].update("")
        predicate = values["-predicate-"]
        window["-predicate-"].update("")
        object = values["-object-"]
        window["-object-"].update("")
        tri_list.append(subject+'->'+predicate+'->'+object)
        window["-result-"].update(tri_list)
    elif event == "-save-":
        filename = str(values["-txt-"]).split("/")[-1][:-4]
        str = '\n'
        f=open(values["-FOLDER-"]+"/"+filename+"_result.txt","w")
        f.write(str.join(tri_list))
        f.close()
        window["-result-"].update("")
        sg.popup_ok("标注结果保存到："+values["-FOLDER-"]+"/"+filename+"_result.txt","保存成功，感谢您的使用！",title='提示',font='微软雅黑')
window.close()





