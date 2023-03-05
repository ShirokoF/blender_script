
#モジュールのインポート
import bpy
import numpy as np
from mathutils import Color


#変数設定
dist = 2.5
fl = 50
numOfPhoto = 1
numOfRot = 2
dTheta = 360./float(numOfPhoto)
theta = 0
pnum = 0
w = 30 
h = 30
randThetaRangeX = 2
randThetaRangeY = 2
randThetaRangeZ = 6
randHeightRange = 0.1
randDistRange = 1
camPos = [dist, 0., 0.5]
cameuler = [np.pi/2., 0., np.pi/2.]
Cone_Ramp=[0,1,0.5]


#アイテムの設定
#bpy.data.objectsの中身はblenderのオブジェクト名にする
camera = bpy.data.objects['Camera']
cone=bpy.data.objects['Cone']
human=bpy.data.objects['human']
tent=bpy.data.objects['tent']
rock1=bpy.data.objects['Rock1']
rock2=bpy.data.objects['Rock2']
branch1=bpy.data.objects['branch1']
branch2=bpy.data.objects['branch2']


#角度に関する定義
def degToRad(deg):
    return np.pi*deg/180.    

#色の変化をリセット
def reset_color():
    res_c=bpy.data.objects['Cone'].color.pos=0.167

    return res_c

#初期位置の設定
def reset_position():
    tent_x=bpy.data.objects['tent'].location.x=-1.0902
    tent_y=bpy.data.objects['tent'].location.y=1.913
    human_x=bpy.data.objects['human'].location.x=-3.4069
    human_y=bpy.data.objects['human'].location.y=0.09949
    rock1_x=bpy.data.objects['Rock1'].location.x=-3.4069
    rock1_y=bpy.data.objects['Rock1'].location.y=0.09949
    rock2_x=bpy.data.objects['Rock2'].location.x=-0.09
    rock2_y=bpy.data.objects['Rock2'].location.y=0.0
    branch1_x=bpy.data.objects['branch1'].location.x=-0.82
    branch1_y=bpy.data.objects['branch1'].location.y=-0.2
    branch2_x=bpy.data.objects['branch2'].location.x=-0.37
    branch2_y=bpy.data.objects['branch2'].location.y=-0.0
    
    bpy.data.materials['cone_mat'].node_tree.nodes['Combine Color'].inputs[1].default_value=0.9

    return tent_x,tent_y,human_x,human_y


#カメラ撮影に関する定義
#座標がランダムになるようにしている
def capture(cam, num, theta, w=30, h=30,rotNum = 4):
    global pnum
    bpy.context.scene.render.resolution_x = w
    bpy.context.scene.render.resolution_y = h  
    for i in range(num+1):
        for j in range(rotNum):
            randRotX = np.random.uniform(-100,100)/100.
            randRotY = np.random.uniform(-100,100)/100.
            randRotZ = np.random.uniform(-100,100)/100. 
            randDist = np.random.uniform(-100,100)/100.
            randHeight = np.random.uniform(-100,100)/100.       
        
            cam.rotation_euler[0] += degToRad(randRotX*randThetaRangeX)
            cam.rotation_euler[1] = degToRad(j*360./rotNum)    
            cam.rotation_euler[2] = degToRad(90+theta+randRotZ*randThetaRangeZ)
            
            
            pos = [(dist+randDist*randDistRange)*np.cos(degToRad(theta)), (dist+randDist*randDistRange)*np.sin(degToRad(theta)), randHeight*randHeightRange] 
               
            cam.location = pos
    
            bpy.ops.render.render()
            bpy.data.images['Render Result'].save_render(filepath = r'C:\Users\fujik\OneDrive\デスクトップ\cansat_ai_test\cone_image_saved\nasi_'+str(1000+pnum)+'.jpg')
                        
            cam.rotation_euler = cameuler
            
            theta += dTheta
        
            pnum+=1
            
#背景に関するリスト
backgroundList = []

#背景をリストに格納する
for i in range(100):
    for j in range(100):
        for k in range(100):
            backgroundList.append([i,j,k])
            

#画像を生成する処理
for i in range(200):
    #object location at random
    bpy.data.objects['tent'].location.x+=np.random.randint(-150,150)/150
    bpy.data.objects['tent'].location.y+=np.random.randint(-150,150)/150
    bpy.data.objects['human'].location.x+=np.random.randint(-150,150)/150
    bpy.data.objects['human'].location.y+=np.random.randint(-150,150)/150
    bpy.data.objects['Rock1'].location.x+=np.random.randint(-150,150)/150
    bpy.data.objects['Rock1'].location.y+=np.random.randint(-150,150)/150
    bpy.data.objects['Rock2'].location.x+=np.random.randint(-150,150)/150
    bpy.data.objects['Rock2'].location.y+=np.random.randint(-150,150)/150    
    bpy.data.objects['branch1'].location.x+=np.random.randint(-150,150)/150
    bpy.data.objects['branch1'].location.y+=np.random.randint(-150,150)/150
    bpy.data.objects['branch2'].location.x+=np.random.randint(-150,150)/150
    bpy.data.objects['branch2'].location.y+=np.random.randint(-150,150)/150
        
    #彩度をランダムにする
    bpy.data.materials['cone_mat'].node_tree.nodes['Combine Color'].inputs[1].default_value= np.random.randint(70,100)/100
        
    
    #背景を変化させる(先ほどリストに入れたものを使う)
    bpy.data.worlds["World"].node_tree.nodes["ミックス.002"].inputs[0].default_value = backgroundList[i][0]
    bpy.data.worlds["World"].node_tree.nodes["ミックス"].inputs[0].default_value = backgroundList[i][1]
    bpy.data.worlds["World"].node_tree.nodes["ミックス.001"].inputs[0].default_value = backgroundList[i][2]
                                                                                        
    #撮影
    capture(camera, numOfPhoto, theta,w,h,numOfRot)

    #全てのオブジェクトの座標を初期位置に戻す
    reset_position()