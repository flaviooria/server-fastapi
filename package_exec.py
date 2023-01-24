import os
from shutil import copy, copytree, move , rmtree
from subprocess import run

if __name__ == '__main__':
    try: 
        exec_name = 'HMI_CREATIO'
        base_path = '/home/creatio/projects'
        exec_path = f'{base_path}/exec'
        diretories_list = ['config','assets','language','dist']

        print('Ejecutandose empaquetador de programa')
        install_requirements = run(['pip','install','-r',f'{base_path}/{exec_name}/requirements.txt'])
        print('requirements result => ',install_requirements)
        if install_requirements.returncode != 0:
            raise Exception('Could not install requirements')

        process = run(['pyinstaller',f'{base_path}/{exec_name}/main.py','--name',exec_name,'--noconsole','--noconfirm','--onefile'])
        if process.returncode == 0:
            if os.path.exists(exec_path):
                rmtree(exec_path)

            print('Copiando archivos')
            for directory in diretories_list:
                if directory == 'dist':
                    copy(f'{base_path}/{exec_name}/{directory}/{exec_name}',f'{exec_path}')
                else:
                    copytree(f'{base_path}/{exec_name}/{directory}',f'{exec_path}/{directory}')
            os.mkdir(f'{exec_path}/logging')
            print('Archivos copiados con éxito')

            print('Empaquetando ejecutable')
            # package = make_archive(f'{exec_name}','zip',base_dir=exec_path)
            package_procces = run(['tar','-czvf',f'{exec_name}-package.tar.gz','-C',base_path,'exec'])

            if package_procces.returncode == 0:
                move(f'./{exec_name}-package.tar.gz','/home/creatio')
                print('Ejecutable comprimido con éxito')
            else:
                print('No se pudo comprimir ejecutable')

        else:
            print('No se pudo empaquetar programa')
        
    except Exception as e:
        print(e)
    
    
