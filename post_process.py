import subprocess
import glob
import os
subprocess.run(['sudo','nvidia-smi','-pm','1'])
number_of_files = 1

for file in glob.glob('/home/ubuntu/*.stl'):
	os.remove(file)

counter=1
while number_of_files>0:
	a=subprocess.check_output(['aws','s3','ls','s3://{bucket_name}/stls/'])
	b=str(a)
	number_of_files = b.count('stl')
	first_index=b.index('.stl')
	c=b[0:first_index]
	d=c[::-1]
	space_index=d.index(' ')
	e=d[0:space_index]
	f=e[::-1]

	subprocess.run(['rm','/home/ubuntu/blender_stuff/output/image1.jpg'])
	subprocess.run(['rm','/home/ubuntu/blender_stuff/output/image2.jpg'])
	subprocess.run(['rm','/home/ubuntu/blender_stuff/output/image3.jpg'])
	subprocess.run(['rm','/home/ubuntu/blender_stuff/output/movie.avi'])
	subprocess.run(['rm','/home/ubuntu/*.stl'])

	subprocess.run(['aws','s3','cp','s3://{bucket_name}/stls/' + str(f) + '.stl','/home/ubuntu/' + str(f) + '.stl'])

	subprocess.run(['blender','-b','/home/ubuntu/blender_stuff/Table_Wooden_Livingroom_MK3Dv2.blend','-P','/home/ubuntu/prep_for_aws_fast.py'])

	subprocess.run(['aws','s3','cp','/home/ubuntu/blender_stuff/output/image1.jpg','s3://{bucket_name}/blender_output/' + str(f) + '/image1.jpg'])
	subprocess.run(['aws','s3','cp','/home/ubuntu/blender_stuff/output/image2.jpg','s3://{bucket_name}/blender_output/' + str(f) + '/image2.jpg'])
	subprocess.run(['aws','s3','cp','/home/ubuntu/blender_stuff/output/image3.jpg','s3://{bucket_name}/blender_output/' + str(f) + '/image3.jpg'])
	subprocess.run(['aws','s3','cp','/home/ubuntu/blender_stuff/output/movie.avi','s3://{bucket_name}/blender_output/' + str(f) + '/movie.avi'])
	subprocess.run(['rm','/home/ubuntu/' + str(f) + '.stl'])
	subprocess.run(['aws','s3','rm','s3://{bucket_name}/stls/' + str(f) + '.stl'])
	subprocess.run(['rm','/home/ubuntu/blender_stuff/output/image1.jpg'])
	subprocess.run(['rm','/home/ubuntu/blender_stuff/output/image2.jpg'])
	subprocess.run(['rm','/home/ubuntu/blender_stuff/output/image3.jpg'])
	subprocess.run(['rm','/home/ubuntu/blender_stuff/output/movie.avi'])

	a=subprocess.check_output(['aws','s3','ls','s3://{bucket_name}/stls/'])
	b=str(a)
	number_of_files = b.count('stl')
	print(counter)
	counter=counter+1

subprocess.run(['aws','ec2','terminate-instances','--instance-ids','i-0710a997053f1ec98'])