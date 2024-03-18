#version 2020/07/05
#Author 先知大人
import numpy as np
import random
import time

'''
#图片转换格式并改变大小的方法：
from PIL import Image
import math
#转换图片

image = Image.open('E://2.png')
image = image.resize((700, 500), Image.ANTIALIAS)
image.save('E://2.ppm')

'''




#首先获取地图中为空的元素(这里表现为0)
def get_null_space(array):
    list_null = []
    for i in range(4):
        for j in range(4):
            if array[i][j]==0:
                list_null.append([i,j])
    return list_null


#随机选取记录空位置列表的某个元素
def random_pick(array):
    record = get_null_space(array)
    len_list_null = len(record)
    random_num = random.randint(0,len_list_null-1)
    random_choice = record[random_num]
    return random_choice


#选择空位置让其变为2或者4
def generate(array):
    record = random_pick(array)
    i = record[0]
    j = record[1]
    array[i][j] = random.randrange(2,5,2)


#移动空位置跳过：气泡浮出
#将列表的气泡浮到最上面或最下面
def single_move(list1,mechanism):
    list_temp = []
    num = 0
    for i in list1:
        if i==0:
            num = num+1
        else:
            list_temp.append(i)
    if mechanism == 0: #下/右
        for j in range(num):
            #在列表开头添加0元素
            list_temp.insert(0,0)
    if mechanism == 1: #上/左
        for j in range(num):
            #在列表结尾添加0元素
            list_temp.append(0)            
    
    return(list_temp)


def bubble(direction,array):
    if direction == 'LEFT':#行操作，mechanism == 1
        for i in range(4):
            list_temp = array[i,:].tolist()
            list_temp = single_move(list_temp,1)
            array[i,:] = np.array(list_temp)
    if direction == 'RIGHT':#行操作，mechanism == 0
        for i in range(4):
            list_temp = array[i,:].tolist()
            list_temp = single_move(list_temp,0)
            array[i,:] = np.array(list_temp)
    if direction == 'UP':#列操作，mechanism == 1
        for i in range(4):
            list_temp = array[:,i].tolist()
            list_temp = single_move(list_temp,1)
            array[:,i] = np.array(list_temp)
    if direction == 'DOWN':#列操作，mechanism == 0
        for i in range(4):
            list_temp = array[:,i].tolist()
            list_temp = single_move(list_temp,0)
            array[:,i] = np.array(list_temp)
        

def single_add(list1,mechanism):
    #list_temp = []
    if mechanism==0:#下，右
        for i in reversed(range(3)):
            if list1[i]==list1[i+1]:
                list1[i+1] = 2*list1[i]
                list1[i]   = 0
                list1 = single_move(list1,0)
            else:
                pass
        return(list1) 
    if mechanism==1:#上，左
        for i in range(3):
            if list1[i]==list1[i+1]:
                list1[i]   = 2*list1[i+1]
                list1[i+1] = 0
                list1 = single_move(list1,1)
            else:
                pass
        return(list1) 
            
        
    
    
def addition(direction,array):
    if direction == 'LEFT':#行操作，mechanism == 1
        for i in range(4):
            list_temp = array[i,:].tolist()
            list_temp = single_add(list_temp,1)
            array[i,:] = np.array(list_temp)
    if direction == 'RIGHT':#行操作，mechanism == 0
        for i in range(4):
            list_temp = array[i,:].tolist()
            list_temp = single_add(list_temp,0)
            array[i,:] = np.array(list_temp)
    if direction == 'UP':#列操作，mechanism == 1
        for i in range(4):
            list_temp = array[:,i].tolist()
            list_temp = single_add(list_temp,1)
            array[:,i] = np.array(list_temp)
    if direction == 'DOWN':#列操作，mechanism == 0
        for i in range(4):
            list_temp = array[:,i].tolist()
            list_temp = single_add(list_temp,0)
            array[:,i] = np.array(list_temp)
        
#获取所有元素，以计算最大值和分数(数字加和)
def get_el(array):
    list_el=[]
    for i in range(4):
        for j in range(4):
            list_el.append(array[i][j])
    return list_el


import tkinter
import tkinter.messagebox
 
root= tkinter.Tk()
root.title('2048')
root.geometry('700x500') #窗口大小

background_image=tkinter.PhotoImage(file="background.ppm")
background_label = tkinter.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


img_up=tkinter.PhotoImage(file="direction\\up.ppm")
img_down=tkinter.PhotoImage(file="E:\\FYwork\\自己的文档ppt\\2048\\direction\\down.ppm")
img_left=tkinter.PhotoImage(file="E:\\FYwork\\自己的文档ppt\\2048\\direction\\left.ppm")
img_right=tkinter.PhotoImage(file="E:\\FYwork\\自己的文档ppt\\2048\\direction\\right.ppm")
#方向键
btn1=tkinter.Button(root,text='UP',   image=img_up   ,command=lambda:Click('UP'),relief="flat")
btn2=tkinter.Button(root,text='DOWN', image=img_down ,command=lambda:Click('DOWN'),relief="flat")
btn3=tkinter.Button(root,text='LEFT', image=img_left ,command=lambda:Click('LEFT'),relief="flat")
btn4=tkinter.Button(root,text='RIGHT',image=img_right,command=lambda:Click('RIGHT'),relief="flat")
btn1.place(x=500,y=50,width=60,height=60)
btn2.place(x=500,y=110,width=60,height=60)
btn3.place(x=440,y=110,width=60,height=60)
btn4.place(x=560,y=110,width=60,height=60)
#重新开始按钮
reset=tkinter.Button(root,text='Restart',bg = 'white',command=lambda:Reset(),font=('Times New Roman',20))
reset.place(x=485,y=200,width=90,height=60)


#游戏开始！      
#生成新的数组（全0）
array1 = np.zeros(shape=(4,4))
#在空位置随机生成新的2/4
generate(array1)


#检查是否达到终止条件:1.达到胜利条件：2048，退出并胜利；2.达到失败条件：满格子且毫无选择，退出并失败；3.没有达到条件，继续游戏
def check():
    max_value = int(max(get_el(array1)))
    if max_value == 2048:#Success
        return 1
    elif check_failure(array1)==4:#Failure
        return 2
    else:
        pass

def check_failure(array):
    #定义标记数，为4表明4方向均无法移动操作
    f_p = 0
    #记录原始数组
    array_temp = array.copy()
    array_temp2 = array.copy()
    
    for direction in ['UP','DOWN','RIGHT','LEFT']:
        
        bubble(direction,array_temp2)
        addition(direction,array_temp2)
        if(get_null_space(array_temp2)==[]):
            f_p += 1
        else:
            pass
        array_temp2 = array_temp.copy()
    
    return f_p
    
        
    
    
    
#重置
def Reset():
    for i in range(4):
        for j in range(4):
            array1[i][j]=0
    generate(array1)
    refresh()


#image 
import math
path = 'E:\\FYwork\\自己的文档ppt\\2048\\'
listname = [ str(int(math.pow(2,i))) for i in range(1,12)]
for i in listname:
    exec('normal_image' + str(i) + ' = ' + 'tkinter.PhotoImage(file = path +str(' +  i  + ') + \'.ppm\')'  )
normal_image0 = tkinter.PhotoImage(file=path+'0.ppm')
#刷新
def refresh():
    for i in range(4):
        for j in range(4):
            tkinter.Label(root, text=int(array1[i][j]),image = eval('normal_image'+str(int(array1[i][j])))).grid(row=i, column=j, padx=0, pady=0)

#每次点击需要进行的事件
#1.移动+加和
#2.新增2/4
#3.刷新显示的数字
#4.判定游戏是否终止（终止需要重置游戏）

refresh()

def Click(direction):
    bubble(direction,array1)
    addition(direction,array1)
    if (get_null_space(array1)!=[]):
        generate(array1)
    else:
        pass
    refresh()
    if check()==1:
        score = int(sum(get_el(array1)))
        result = tkinter.messagebox.askokcancel(title = 'Game over',message='Success ! Your score is '+str(score))
        print(result)
        Reset()
    if check()==2:
        score = int(sum(get_el(array1)))
        result = tkinter.messagebox.askokcancel(title = 'Game over',message='Failure ! Your score is '+str(score))
        print(result)
        Reset()
    else:
        pass
    
    

root.mainloop()