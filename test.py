import subprocess
import os
for i in range(159):
  print(i)
  in_file=f'inputs/input-{i}.txt'
  obj_file=f'obj2/obj-{i}.obj'
  err_file=f'er2/err-{i}.txt'
  out_file=f'out2/output-{i}.txt' 
  last_line=''
  try:
    subprocess.run(["python", "hw5.py", "-compile", in_file, obj_file], check=True, capture_output=True, text=True)
    try:
      subprocess.run(["python", "hw5.py", "-execute", obj_file, out_file], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
      last_line = e.stderr.strip().split("\n")[-1]
  except subprocess.CalledProcessError as e:
    last_line = e.stderr.strip().split("\n")[-1]
  if last_line!='':
    f=open(err_file,'w')
    f.write(last_line)
    f.close()