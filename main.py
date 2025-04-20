#this is a test wooooooo

import bpy
import time
import bmesh
import sys
import os
import glob
import subprocess
from bpy import context
from mathutils import Vector
from bmesh.types import BMVert
#bpy.ops.text.save()
#bpy.ops.wm.save_mainfile()
from bpy_extras.object_utils import world_to_camera_view

try:
	bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
	bpy.context.user_preferences.addons['cycles'].preferences.devices[1].use= True
	print(bpy.context.user_preferences.addons['cycles'].preferences.devices[1])
	bpy.context.scene.cycles.device = 'GPU'
	bpy.context.scene.render.tile_x = 256
	bpy.context.scene.render.tile_y = 256
	print("GPU selected!")
	
except:
	print("no gpu :( poooo")
	time.sleep(5)

print("Number of threads is: ", bpy.data.scenes["Scene"].render.threads)

#############################USER INPUT#####################################
pointer_to_filepath="filepath"
filenamelist=glob.glob('/home/ubuntu/*.stl')
z_offset=.456

material=1

#IMPORT TEXTURE INFORMATION FOR HTE PLANE

for aa in filenamelist:
    filename=aa
    height=.15
    #############################USER INPUT#####################################

    def kill_all():
        subprocess.run(['aws','ec2','terminate-instances','--instance-ids','i-0710a997053f1ec98'])

    #############################FUNCTION FOR CLEARING WORKSPACE####################################
    def delete_stuff():

        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            print("In object mode")

        try:
            for obj in bpy.data.objects:
                if "new" in obj.name: 
                    print("object name :", obj.name)   
                    obj.select=True     
                    bpy.data.objects.remove(obj,do_unlink=True)
        except:
            print("no object")
            
        try:
            for cam in bpy.data.cameras:
                bpy.data.cameras.remove(cam)
                print("deleted")
        except:
            print("no camera")

        try:
            for thing in bpy.data.curves:
                bpy.data.curve.remove(thing)
                print("deleted curves")
        except:
            print("no curves")
            
        try:
            for thing in bpy.data.planes:
                bpy.data.plane.remove(thing)
                print("deleted planes")
        except:
            print("no planes")

        for m in bpy.data.materials:
            if "new" in m.name:
                bpy.data.materials.remove(m)
                print("removed material")
            else:
                print("skipped")
    #############################FUNCTION FOR CLEARING WORKSPACE####################################


    def create_Vertices (name, verts):
        # Create mesh and object
        me = bpy.data.meshes.new(name+'Mesh')
        ob = bpy.data.objects.new(name + 'new', me)
        ob.show_name = True
        # Link object to scene
        bpy.context.scene.objects.link(ob)
        me.from_pydata(verts, [], [])
        # Update mesh with new data
        me.update()
        return ob
   #############################FUNCTION FOR finding vertices####################################
    def vertex_stuff(obj,cam):
        mesh = obj.data
        mat_world = obj.matrix_world
        cs, ce = cam.data.clip_start, cam.data.clip_end
        scene = bpy.context.scene
        bpy.context.scene.objects.active=obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(mesh)
        i=0
        j=0
        m=0
        n=0
        o=0
        p=0
        for v in bm.verts:
            co_ndc = world_to_camera_view(scene, cam, mat_world * v.co)
            #check wether point is inside frustum
            if (0.0 < co_ndc.x < 1.0 and
                0.0 < co_ndc.y < 1.0 and
                 cs < co_ndc.z <  ce):
                v.select = True
                i+=1
            else:
                j+=1
                v.select = False
            if (co_ndc.y < 0.05):
                m+=1
            if (co_ndc.y > 0.95):
                n+=1
            if (co_ndc.x < 0.05):
                o+=1
            if (co_ndc.x > 0.95):
                p+=1
        bmesh.update_edit_mesh(mesh, False, False)
        return (i,j,m,n,o,p)
   #############################FUNCTION FOR zooming####################################
    def zoom(cam,obj):
        counter=0
        while True:
            [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            if counter==0:
                oldj=1
                oldi=i+j
                #already zoomed out
                if j==0 and i==i+j:
                    while j==0:
                        bpy.data.cameras[cam.name].ortho_scale-=.2#zoom in
                        [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            if j>0 or oldj>0: 
                bpy.data.cameras[cam.name].ortho_scale+=.2#zoom out
            elif i<=i+j or oldi<=i+j: 
                bpy.data.cameras[cam.name].ortho_scale-=.2#zoom in
                
                
            if j==0 and oldj==0:#all the way zoomed out-go back one setp
                bpy.data.cameras[cam.name].ortho_scale+=.2
                break
            if i==i+j and oldi==i+j:#all the way zoomed in - go back one setp
                #bpy.data.cameras[cam.name].ortho_scale-=20
                break
            if j==0 and i==0:
                raise RuntimeError('there are no vertices!')
            oldj=j
            oldi=i
            counter=counter+1
            if counter>1000:
                        kill_all()
            print("i is: ",i," j is ",j," counter is: ", counter)
            if cam.name=="Camera.003":
                bpy.data.cameras[cam.name].ortho_scale+=.2#zoom out
                
                
   #############################FUNCTION FOR panning up and down####################################            
    def panupdown(cam,obj,dimensions,scale):
        counter=0
        flag1=0
        flag2=0
        orig_scale=bpy.data.cameras[cam.name].ortho_scale
        #orig_location=bpy.data.objects[cam.name].location
        #bpy.data.objects[cam.name].location[2]=dimensions[2]*scale/2
        while True:
            current_rotation=bpy.data.objects[cam.name].rotation_euler
            #bpy.data.cameras[cam.name].ortho_scale=orig_scale*5
            #bpy.data.cameras[cam.name].ortho_scale=orig_scale*5
            if counter==0:
                [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            if j>0 and counter ==0:
                while j>0:
                    bpy.data.cameras[cam.name].ortho_scale+=bpy.data.cameras[cam.name].ortho_scale*.25
                    print("expanding field")
                    [i,j,m,n,o,p]=vertex_stuff(obj,cam)
                bpy.data.cameras[cam.name].ortho_scale+=bpy.data.cameras[cam.name].ortho_scale*.25
            [i,j,m,n,o,p]=vertex_stuff(obj,cam)    
            if flag1==0 and flag2==0 and j==0:
                    bpy.data.objects[cam.name].rotation_euler=(current_rotation[0]+2*3.1415/180,current_rotation[1],current_rotation[2])
                    print("moving up")
            elif flag1==1 and flag2==0 and j==0:
                    bpy.data.objects[cam.name].rotation_euler=(current_rotation[0]-2*3.1415/180,current_rotation[1],current_rotation[2])
                    print("movind down")
            [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            
            if j>0 and flag1==0 and flag2==0:
                flag1=1
                angle1=bpy.data.objects[cam.name].rotation_euler[0]
                bpy.data.objects[cam.name].rotation_euler=(current_rotation[0]-2*3.1415/180,current_rotation[1],current_rotation[2])
            elif j>0 and flag2==0 and flag1==1:
                flag2=1
                angle2=bpy.data.objects[cam.name].rotation_euler[0]
                
#            if p>1 and o>1:
#                bpy.data.cameras[cam.name].ortho_scale+=bpy.data.cameras[cam.name].ortho_scale*.1
#                print("expanding field -again")

            if flag1==1 and flag2==1:
                angle1deg=angle1
                angle2deg=angle2
                angletotal=(angle1deg+angle2deg)/2
                #bpy.data.objects[cam.name].location=orig_location
                bpy.data.objects[cam.name].rotation_euler=(angletotal,current_rotation[1],current_rotation[2])
                bpy.data.cameras[cam.name].ortho_scale=orig_scale
                break
            if j==0 and i==0:
                raise RuntimeError('there are no vertices!')
            counter=counter+1
            if counter>1000:
                        kill_all()
            print("m is: ",m," n is ",n," counter is: ", counter) 
            
   #############################FUNCTION FOR adding material for the plane####################################            
    def material_plane(mat_name2):
        #CREATE THE NODES FOR THE PLANE
        bpy.data.materials[mat_name2].node_tree.nodes.new(type="ShaderNodeMixShader")
        bpy.data.materials[mat_name2].node_tree.nodes.new(type="ShaderNodeBsdfGlossy")
        bpy.data.materials[mat_name2].node_tree.nodes.new(type="ShaderNodeNormalMap")
        bpy.data.materials[mat_name2].node_tree.nodes.new(type="ShaderNodeTexImage")
        bpy.data.materials[mat_name2].node_tree.nodes.new(type="ShaderNodeTexImage")
        inp=bpy.data.materials[mat_name2].node_tree.nodes['Material Output'].inputs['Surface']
        outp=bpy.data.materials[mat_name2].node_tree.nodes['Mix Shader'].outputs['Shader']
        inpMix=bpy.data.materials[mat_name2].node_tree.nodes['Mix Shader'].inputs[2]
        outpgloss=bpy.data.materials[mat_name2].node_tree.nodes['Glossy BSDF'].outputs['BSDF']
        inpMix2=bpy.data.materials[mat_name2].node_tree.nodes['Mix Shader'].inputs[1]
        outpdiffuse=bpy.data.materials[mat_name2].node_tree.nodes['Diffuse BSDF'].outputs['BSDF']
        inppdiffuse=bpy.data.materials[mat_name2].node_tree.nodes['Diffuse BSDF'].inputs['Normal']
        inppdiffuse2=bpy.data.materials[mat_name2].node_tree.nodes['Diffuse BSDF'].inputs['Color']
        inpglossy=bpy.data.materials[mat_name2].node_tree.nodes['Glossy BSDF'].inputs['Normal']
        outnormal=bpy.data.materials[mat_name2].node_tree.nodes['Normal Map'].outputs['Normal']
        outnormal2=bpy.data.materials[mat_name2].node_tree.nodes['Normal Map'].outputs['Normal']
        innormal=bpy.data.materials[mat_name2].node_tree.nodes['Normal Map'].inputs['Color']
        outimagetexture1=bpy.data.materials[mat_name2].node_tree.nodes[6].outputs['Color']
        outimagetexture2=bpy.data.materials[mat_name2].node_tree.nodes[5].outputs['Color']


        #CONNECT ALL THE NODES FOR THE PLANE
        bpy.data.materials[mat_name2].node_tree.links.new(inp,outp)
        bpy.data.materials[mat_name2].node_tree.links.new(innormal,outimagetexture1)
        bpy.data.materials[mat_name2].node_tree.links.new(inppdiffuse2,outimagetexture2)#this is #5, diffuse
        bpy.data.materials[mat_name2].node_tree.links.new(inpMix,outpgloss)
        bpy.data.materials[mat_name2].node_tree.links.new(inpMix2,outpdiffuse)
        bpy.data.materials[mat_name2].node_tree.links.new(outnormal,inpglossy)
        bpy.data.materials[mat_name2].node_tree.links.new(outnormal2,inppdiffuse)
        bpy.data.materials[mat_name2].node_tree.nodes['Glossy BSDF'].inputs[0].default_value = (0.1034,0.0504,0.0554,1)
        bpy.data.materials[mat_name2].node_tree.nodes['Glossy BSDF'].inputs[1].default_value = (0.025)
        bpy.data.materials[mat_name2].node_tree.nodes['Mix Shader'].inputs[0].default_value = .1
        bpy.data.materials[mat_name2].node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = (0.216,0.125,0.0314,1)
        bpy.data.materials[mat_name2].node_tree.nodes['Diffuse BSDF'].inputs[1].default_value = (.1)
        bpy.data.materials[mat_name2].node_tree.nodes['Image Texture.001'].color_space = "NONE"
        
        bpy.data.objects[obj].active_material=bpy.data.materials[mat_name]
        bpy.data.materials[mat_name2].node_tree.nodes['Image Texture'].image=bpy.data.images.load(filepath_for_textures + filename_for_color)
        bpy.data.materials[mat_name2].node_tree.nodes['Image Texture.001'].image=bpy.data.images.load(filepath_for_textures + filename_for_norm)           

#############################FUNCTION FOR assigning material to object####################################
    def material_object(mat_name):
             #ASSIGN/CREATE HTE NODES FOR HTE MODEL
        bpy.data.materials[mat_name].node_tree.nodes.new(type="ShaderNodeMixShader")
        bpy.data.materials[mat_name].node_tree.nodes.new(type="ShaderNodeBsdfGlossy")
        bpy.data.materials[mat_name].node_tree.nodes.new(type="ShaderNodeTexWave")
        bpy.data.materials[mat_name].node_tree.nodes.new(type="ShaderNodeMapping")
        bpy.data.materials[mat_name].node_tree.nodes.new(type="ShaderNodeTexCoord")
        inp=bpy.data.materials[mat_name].node_tree.nodes['Material Output'].inputs['Surface']
        outp=bpy.data.materials[mat_name].node_tree.nodes['Mix Shader'].outputs['Shader']
        inpMix=bpy.data.materials[mat_name].node_tree.nodes['Mix Shader'].inputs[2]
        outpgloss=bpy.data.materials[mat_name].node_tree.nodes['Glossy BSDF'].outputs['BSDF']
        inpMix2=bpy.data.materials[mat_name].node_tree.nodes['Mix Shader'].inputs[1]
        outpdiffuse=bpy.data.materials[mat_name].node_tree.nodes['Diffuse BSDF'].outputs['BSDF']
        inpwave=bpy.data.materials[mat_name].node_tree.nodes['Wave Texture'].inputs['Vector']
        outwave=bpy.data.materials[mat_name].node_tree.nodes['Wave Texture'].outputs['Color']
        inpglossy=bpy.data.materials[mat_name].node_tree.nodes['Glossy BSDF'].inputs['Roughness']
        outmap=bpy.data.materials[mat_name].node_tree.nodes['Mapping'].outputs['Vector']
        inwave=bpy.data.materials[mat_name].node_tree.nodes['Wave Texture'].inputs['Vector']
        outcoord=bpy.data.materials[mat_name].node_tree.nodes['Texture Coordinate'].outputs['Generated']
        inmap=bpy.data.materials[mat_name].node_tree.nodes['Mapping'].inputs['Vector']
        bpy.data.materials[mat_name].node_tree.nodes['Mapping'].rotation[2]=45*3.14/180
        bpy.data.materials[mat_name].node_tree.nodes['Mapping'].scale[2]=20
        #CONNECT ALL THE NODES
        bpy.data.materials[mat_name].node_tree.links.new(inp,outp)
        bpy.data.materials[mat_name].node_tree.links.new(inpMix,outpgloss)
        bpy.data.materials[mat_name].node_tree.links.new(inpMix2,outpdiffuse)
        bpy.data.materials[mat_name].node_tree.links.new(outwave,inpglossy)
        bpy.data.materials[mat_name].node_tree.links.new(outmap,inwave)
        bpy.data.materials[mat_name].node_tree.links.new(outcoord,inmap)
        bpy.data.materials[mat_name].node_tree.nodes['Glossy BSDF'].inputs[0].default_value = (0.09,0.0539,0.015,1)
        bpy.data.materials[mat_name].node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = (0.216,0.125,0.0314,1)
        bpy.data.materials[mat_name].node_tree.nodes['Diffuse BSDF'].inputs[1].default_value = 0.75          
                
    def panleftright(cam,obj,dimensions,scale):
        counter=0
        flag1=0
        flag2=0
        orig_scale=bpy.data.cameras[cam.name].ortho_scale
        #orig_location=bpy.data.objects[cam.name].location
        #bpy.data.objects[cam.name].location[2]=dimensions[2]*scale/2
        while True:
            current_rotation=bpy.data.objects[cam.name].rotation_euler
            #bpy.data.cameras[cam.name].ortho_scale=orig_scale/10
            #bpy.data.cameras[cam.name].ortho_scale=orig_scale*5
            if counter==0:
                [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            if j>0:
                while j>0:
                    bpy.data.cameras[cam.name].ortho_scale+=bpy.data.cameras[cam.name].ortho_scale*.25
                    print("expanding field")
                    [i,j,m,n,o,p]=vertex_stuff(obj,cam)
                bpy.data.cameras[cam.name].ortho_scale+=bpy.data.cameras[cam.name].ortho_scale*.25
                
            if flag1==0 and flag2==0:
                    bpy.data.objects[cam.name].rotation_euler=(current_rotation[0],current_rotation[1],current_rotation[2]-.5*3.1415/180)
            elif flag1==1 and flag2==0:
                    bpy.data.objects[cam.name].rotation_euler=(current_rotation[0],current_rotation[1],current_rotation[2]+.5*3.1415/180)
            
            [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            
            if o>0 and flag1==0 and flag2==0:
                flag1=1
                angle1=bpy.data.objects[cam.name].rotation_euler[2]
                
            if p>0 and flag2==0 and flag1==1:
                flag2=1
                angle2=bpy.data.objects[cam.name].rotation_euler[2]
                
            if p>1 and o>1:
                bpy.data.cameras[cam.name].ortho_scale+=bpy.data.cameras[cam.name].ortho_scale*.1
                print("expanding field -again")

            if flag1==1 and flag2==1:
                angle1deg=angle1
                angle2deg=angle2
                angletotal=(angle1deg+angle2deg)/2
                #bpy.data.objects[cam.name].location=orig_location
                bpy.data.objects[cam.name].rotation_euler=(current_rotation[0],current_rotation[1],angletotal)
                bpy.data.cameras[cam.name].ortho_scale=orig_scale
                break
            if j==0 and i==0:
                raise RuntimeError('there are no vertices!')
            counter=counter+1
            if counter>1000:
                        kill_all()
            print("o is: ",m," p is ",n," counter is: ", counter)  
     
            
    def zoom_persp(cam,obj):
        counter=0
        bpy.data.cameras[cam.name].type="PERSP"
        
        while True:
            [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            if counter==0:
                oldj=1
                oldi=i+j
                #already zoomed out
                if j==0 and i==i+j:
                    while j==0:
                        bpy.data.cameras[cam.name].lens+=10#zoom in
                        [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            if j>0 or oldj>0: 
                bpy.data.cameras[cam.name].lens-=10#zoom out
                print("zoom out")
            elif i<=i+j or oldi<=i+j: 
                bpy.data.cameras[cam.name].lens+=10#zoom in
                print("zoom in")
                
            if j==0 and oldj==0:#all the way zoomed out-go back one setp
                bpy.data.cameras[cam.name].lens-=10
                break
            if i==i+j and oldi==i+j:#all the way zoomed in - go back one setp
                #bpy.data.cameras[cam.name].ortho_scale-=20
                break
            if j==0 and i==0:
                raise RuntimeError('there are no vertices!')
            oldj=j
            oldi=i
            counter=counter+1
            if counter>1000:
                        kill_all()
            print("i is: ",i," j is ",j," counter is: ", counter)
            if cam.name=="Camera.003":
                bpy.data.cameras[cam.name].lens-=5#zoom out


    def panleftright_persp(cam,obj,dimensions,scale):
        counter=0
        flag1=0
        flag2=0
        
        #orig_location=bpy.data.objects[cam.name].location
        #bpy.data.objects[cam.name].location[2]=dimensions[2]*scale/2
        while True:
            current_rotation=bpy.data.objects[cam.name].rotation_euler
            
            #bpy.data.cameras[cam.name].ortho_scale=orig_scale*5
            if counter==0:
                [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            if j>0 and counter ==0:
                while j>0:
                    bpy.data.cameras[cam.name].lens-=bpy.data.cameras[cam.name].lens*.2
                    print("expanding field-persp")
                    [i,j,m,n,o,p]=vertex_stuff(obj,cam)
                bpy.data.cameras[cam.name].lens-=bpy.data.cameras[cam.name].lens*.2
            [i,j,m,n,o,p]=vertex_stuff(obj,cam)   
            if flag1==0 and flag2==0 and j==0:
                    bpy.data.objects[cam.name].rotation_euler=(current_rotation[0],current_rotation[1],current_rotation[2]-.1*3.1415/180)
                    print("rotating right - persp",((current_rotation[2]-.1*3.1415/180)*180/3.1415))
            elif flag1==1 and flag2==0 and j==0:
                    bpy.data.objects[cam.name].rotation_euler=(current_rotation[0],current_rotation[1],current_rotation[2]+.1*3.1415/180)
                    print("rotating left - persp ",((current_rotation[2]+.1*3.1415/180)*180/3.1415))
                    
            [i,j,m,n,o,p]=vertex_stuff(obj,cam)
            
            if j>0 and flag1==0 and flag2==0:
                flag1=1
                angle1=bpy.data.objects[cam.name].rotation_euler[2]
                bpy.data.objects[cam.name].rotation_euler=(current_rotation[0],current_rotation[1],current_rotation[2]+.1*3.1415/180)
            elif j>0 and flag2==0 and flag1==1:
                flag2=1
                angle2=bpy.data.objects[cam.name].rotation_euler[2]
                
#            if p>1 and o>1:
#                bpy.data.cameras[cam.name].lens-=bpy.data.cameras[cam.name].lens*.1
#                print("expanding field -again")

            if flag1==1 and flag2==1:
                angle1deg=angle1
                angle2deg=angle2
                angletotal=(angle1deg+angle2deg)/2
                #bpy.data.objects[cam.name].location=orig_location
                bpy.data.objects[cam.name].rotation_euler=(current_rotation[0],current_rotation[1],angletotal)
                
                break
            if j==0 and i==0:
                raise RuntimeError('there are no vertices!')
            counter=counter+1
            if counter>1000:
                        kill_all()
            print("o is: ",m," p is ",n," counter is: ", counter)  
     
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
    delete_stuff()
    
    bpy.context.scene.world.horizon_color = (0.633209, 0.633209, 0.633209)

    #SET RENDERING ENGINE
    #bpy.data.scenes["Scene"].render.engine='CYCLES'

    #SET UNIT LENGTH TO MILLIMETERS
    #bpy.ops.script.python_file_run(filepath="C:\\Program Files\\Blender Foundation\\Blender\\2.79\\scripts\\presets\\units_length\\meters.py")
    scene = bpy.context.scene

    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0

    #IMPORT THE MODEL
    #bpy.ops.import_mesh.stl(filepath=("C://Users//Administrator//Desktop//" + filename + ".stl"),axis_forward='-Z',axis_up='-Y',global_scale=1)
    bpy.ops.import_mesh.stl(filepath=(filename),axis_forward='-Z',axis_up='-Y',global_scale=1)

    #CHANGE TO EDMIT MODE
    bpy.ops.object.mode_set(mode='EDIT')
    
    #ASSIGN OBJECT AS THE NAME OF THE MODEL
    bpy.context.scene.objects.active.name=bpy.context.scene.objects.active.name + "new"
    obj=bpy.context.scene.objects.active.name 
    obj_obj=bpy.context.scene.objects.active

    #IMPORT THE MESH DATA FROM THE MODEL
    mesh=obj_obj.data

    #VECTORS CONTAINING THE X,Y, AND Z COORDINATES OF ALL THE VERTICES IN THE MODEL
    xvector=[]
    yvector=[]
    zvector=[]

    #LOOP THROUGH THE VERTICES AND GET THEIR COORDINATES AND RECORD THEM
    for vert in mesh.vertices:
        xvector.append(vert.co.x)
        yvector.append(vert.co.y)
        zvector.append(vert.co.z)
      
    #FIND THE MIN AND MAX OF EACH OF THE VECTORS  
    xmin=min(xvector)
    xmax=max(xvector)
    ymin=min(yvector)
    ymax=max(yvector)
    zmin=min(zvector)
    zmax=max(zvector)

    #CHANGE BACK TO OBJECT MODE
    bpy.ops.object.mode_set(mode='OBJECT')

    #CREATE A VECTOR WITH THE DIMENSIONS OF THE OBJECT
    dimensions=[abs(xmax-xmin),abs(ymax-ymin),abs(zmax-zmin)]

    #FIND THE SCALE FOR ADJUSTING THE HEIGHT OF THE MODEL TO THE DESIRED HEIGHT
    scale=height/dimensions[2]

    #SCALE THE MODEL
    bpy.data.objects[obj].scale[0]=scale
    bpy.data.objects[obj].scale[1]=scale
    bpy.data.objects[obj].scale[2]=scale

    scaler=(dimensions[0]*dimensions[2]*scale*scale)#get the maximum dimension of the model for sizing everything else
    #units in mm
    print("largest dimension is: ", scaler)

    #CHANGE THE LOCATION OF THE MODEL TO COINCIDE WITH THE DIMENSIONS
    bpy.data.objects[obj].location=((-xmax+dimensions[0]/2)*scale,(-ymax+dimensions[1]/2)*scale,z_offset+((-zmax+dimensions[2])*scale)-(dimensions[2]*scale*0.01))

    #CHANGE THE RENDERING TO SMOOTH
    bpy.ops.object.shade_smooth()

    #SAVE THE LOCATION DATA INTO A VARIABLE
    location=bpy.data.objects[obj].location

    #ASSIGN THE MATERIAL NAME FOR THE MODEL
    mat_name="mat1new"
    mat=bpy.data.materials.new(mat_name)
    #TURN ON THE NODES
    bpy.data.materials[mat_name].use_nodes=True
    material_object(mat_name)
    obj_obj.data.materials.append(mat)
   
    #MATERIAL FOR HTE PLANE
    #mat_name2="mat2new"
    #mat2=bpy.data.materials.new(mat_name2)
    #bpy.data.materials[mat_name2].use_nodes=True
    #material_plane(mat_name2)


    ###########################################ADD CAMERAS##############################################
    name=create_Vertices("pointtest",[location])


    bpy.ops.object.camera_add()
    cam1=bpy.data.cameras[0]
    bpy.data.objects[cam1.name].location=(0,scaler*100,dimensions[2]*scale*10)
    bpy.data.objects[cam1.name].rotation_euler=(-275/180*3.14159,360/180*3.14159,180/180*3.14159)
    bpy.data.objects[cam1.name].scale=bpy.data.objects[cam1.name].scale*.01
    bpy.data.cameras[cam1.name].dof_object=obj_obj
    bpy.data.cameras[cam1.name].clip_end=3
    bpy.data.cameras[cam1.name].type="ORTHO"
    bpy.data.cameras[cam1.name].ortho_scale=dimensions[1]*scale*1.414*1.1

    #ADD CAMERA 2
    bpy.ops.object.camera_add()
    cam2=bpy.data.cameras[1]
    bpy.data.objects[cam2.name].location=(-scaler*100,0,dimensions[2]*scale*10)
    bpy.data.objects[cam2.name].rotation_euler=(265/180*3.14159,180/180*3.14159,90/180*3.14159)
    bpy.data.objects[cam2.name].scale=bpy.data.objects[cam2.name].scale*.01
    bpy.data.cameras[cam2.name].dof_object=obj_obj
    bpy.data.cameras[cam2.name].clip_end=3
    bpy.data.cameras[cam2.name].type="ORTHO"
    bpy.data.cameras[cam2.name].ortho_scale=dimensions[1]*scale*1.414*1.1

    #ADD CAMERA 3
    bpy.ops.object.camera_add()
    cam3=bpy.data.cameras[2]
    bpy.data.objects[cam3.name].location=(0,0,dimensions[2]*scale*20)
    bpy.data.objects[cam3.name].rotation_euler=(-360/180*3.14159,360/180*3.14159,(45+180)/180*3.14159)
    bpy.data.objects[cam3.name].scale=bpy.data.objects[cam2.name].scale*.01
    bpy.data.cameras[cam3.name].dof_object=obj_obj
    bpy.data.cameras[cam3.name].clip_end=3
    bpy.data.cameras[cam3.name].type="ORTHO"
    bpy.data.cameras[cam3.name].ortho_scale=dimensions[1]*scale*1.414*1.1

    #ADD CAMERA 4
    bpy.ops.object.camera_add()
    cam4=bpy.data.cameras[3]
    bpy.data.objects[cam4.name].location=(0,-scaler*100,dimensions[2]*scale*10)
    bpy.data.objects[cam4.name].rotation_euler=(-277/180*3.14159,360/180*3.14159,360/180*3.14159)
    bpy.data.objects[cam4.name].scale=bpy.data.objects[cam1.name].scale
    bpy.data.cameras[cam4.name].dof_object=name
    bpy.data.cameras[cam4.name].clip_end=3
    bpy.data.cameras[cam4.name].type="ORTHO"
    bpy.data.cameras[cam4.name].ortho_scale=dimensions[1]*scale*1.414*1.1
    

#    ###############ensure that the whole model is in FOV

    obj = obj_obj

    #check if need to zoom in or out

    #if need to zoom, then zoom in direction.  If all vertices are in the field, then zoom in until they
    #start to disappear.  If they aren't, then zoom out until they are all there
    cam = bpy.data.objects['Camera']
    zoom(cam,obj)
    panupdown(cam,obj,dimensions,scale)
    panleftright(cam,obj,dimensions,scale)
    zoom_persp(cam,obj)
    panleftright_persp(cam,obj,dimensions,scale)
    zoom_persp(cam,obj)
    
    print("Camera1")
    cam = bpy.data.objects['Camera.001']
    zoom(cam,obj)
    panupdown(cam,obj,dimensions,scale)
    panleftright(cam,obj,dimensions,scale)
    zoom_persp(cam,obj)
    panleftright_persp(cam,obj,dimensions,scale)
    zoom_persp(cam,obj)

    print("Camera2")
    cam = bpy.data.objects['Camera.002']
    zoom(cam,obj)
    panupdown(cam,obj,dimensions,scale)
    

    
    

    print("Camera4")
    ##check for x rotation - move camera until it hits the edge.  Mark the angle.  Then move until it hits the 
    ##other edge.  Then mark that angle.  Find the midpoint between the two angles and assign it to the camera

    #check for z rotation - same as x rotation, but different axis
    bpy.ops.object.mode_set(mode='OBJECT')
    #CREATE CURVE FOR THE ANIMATION
    bpy.ops.curve.primitive_bezier_circle_add(radius=dimensions[0]*scale*2,location=(0,0,dimensions[2]*scale+z_offset))
    bpy.context.scene.objects.active.name=bpy.context.scene.objects.active.name + "new"
    curve_name=bpy.context.scene.objects.active.name
    curve=bpy.data.objects[curve_name]
    cam4_obj=bpy.data.objects["Camera.003"]
    curve.select=True
    cam4_obj.select=True
    #ASSIGN CURVE TO BE PARENT OF CAMERA 4
    cam4_obj.parent=curve
    bpy.context.scene.objects.active=curve
    #ASSIGN CAMERA TO FOLLOW CURVE
    bpy.ops.object.parent_set(type='FOLLOW')
    curve.data.path_duration=200
    curve.data.eval_time=136

   
    bpy.ops.object.mode_set(mode='OBJECT')

    #############################################RENDERING#########################################################
    bpy.ops.object.mode_set(mode='OBJECT')
    #RENDERING SETTINGS
    bpy.data.scenes["Scene"].cycles.use_animated_seed = True
    bpy.data.scenes["Scene"].cycles.seed= 1
    bpy.data.scenes["Scene"].cycles.sample_clamp_direct=0.45
    bpy.data.scenes["Scene"].cycles.sample_clamp_indirect=0.35

    newpath = "//output"
    try:
        os.makedirs(newpath)
    except:
        print("do nothing")


    #PERFORM RENDER 1
    bpy.data.scenes["Scene"].camera=bpy.data.objects[cam1.name]
    bpy.data.scenes["Scene"].render.image_settings.file_format='JPEG'
    bpy.data.scenes['Scene'].render.filepath = newpath + "//"+ 'image1.jpg'
    #plane_obj.rotation_euler[2]=3.1415
    bpy.data.scenes["Scene"].cycles.samples = 800
    bpy.ops.render.render( write_still=True ) 

    ##PEROFRM RENDER 2
    bpy.data.scenes["Scene"].camera=bpy.data.objects[cam2.name]
    bpy.data.scenes["Scene"].render.image_settings.file_format='JPEG'
    bpy.data.scenes['Scene'].render.filepath = newpath +"//"+ 'image2.jpg'
    #plane_obj.rotation_euler[2]=270*3.1415/180
    bpy.data.scenes["Scene"].cycles.samples = 800
    bpy.ops.render.render( write_still=True ) 

    ##PERFORM RENDER 30
    bpy.data.scenes["Scene"].camera=bpy.data.objects[cam3.name]
    bpy.data.scenes["Scene"].render.image_settings.file_format='JPEG'
    bpy.data.scenes['Scene'].render.filepath = newpath + "//"+ 'image3.jpg'
    bpy.data.scenes["Scene"].cycles.samples = 800
    bpy.ops.render.render( write_still=True )
 
    print("Camera4")
    cam = bpy.data.objects['Camera.003']
    bpy.context.scene.frame_set(78)
    zoom(cam,obj)
    panupdown(cam,obj,dimensions,scale)
    panleftright(cam,obj,dimensions,scale)
    zoom_persp(cam,obj)
    panleftright_persp(cam,obj,dimensions,scale)
    zoom_persp(cam,obj)

    print("Camera4")
    bpy.ops.object.mode_set(mode='OBJECT')
    ##PERFORM RENDER 4 (ANIMATION)
    bpy.data.scenes["Scene"].camera=bpy.data.objects[cam4.name]
    bpy.data.scenes["Scene"].render.image_settings.file_format='AVI_JPEG'
    bpy.data.scenes["Scene"].render.image_settings.quality=100
    bpy.data.scenes["Scene"].render.fps=24
    bpy.data.scenes["Scene"].frame_start=44
    bpy.data.scenes["Scene"].frame_end=105
    bpy.data.scenes['Scene'].render.filepath = newpath + "//"+ 'movie.avi'
    #plane_obj.rotation_euler[2]=240*3.1415/180
    bpy.data.scenes["Scene"].cycles.samples = 200
    bpy.ops.render.render( animation=True) 



