import os
import sys
import subprocess
import shlex
import shutil
from contextlib import redirect_stdout

stdout_fd = sys.stdout.fileno()
# commands to execute for environment management
crt_env = "virtualenv"    # pls provide the command to execute
act_env = "activate.bat"
deact_env = "deactivate_env"
instl_pkg = "pip install"
uninstl_pkg = "pip uninstall -y"
list_pkg = "pip freeze >"

# variables for use during environment management
proj_path = os.getcwd()
env_nm = "proj_env2"      # please provide the env folder name
instl_packg = []    # Package to be installed in virtual environment
uninstall_pckg = ["pytz", "KING", "pytest"]   # Package to be uninstalled in virtual environment
req_file = "requirements.txt"


def exec_cmd(cmd, *args, path=None):
    stat = []
    if len(cmd.split())>1:
        param = shlex.split(cmd)
        for val in param:
            stat.append(val)
    else:
        stat.append(cmd)
    if args is not None:
        for val in args:
            stat.append(val)
    print(stat)
    with subprocess.Popen(stat, cwd=path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        id = proc.pid
        op, error_dtl = proc.communicate()
    print("process_id:", id)
    print(op, error_dtl)
    if proc.returncode:
        print('commit failed \n')
    else:
        print('Commit done',proc.returncode)
        print("\n")


def create_env():
    print("Create environment process starts...")
    os.chdir(proj_path)
    exec_cmd(crt_env, env_nm)
    print("create environment process completed..!!")


def check_pkg(pkg):
    files = os.listdir()
    if req_file in files:
        with open(req_file, "r") as file:
            data = file.readlines()
            for line in data:
                if pkg in line:
                    return True
            return False
    else:
        return False


def manage_env():
    print("\nmanage environment process starts..")
    env_path = os.path.join(proj_path, env_nm, "Scripts")
    os.chdir(env_path)
    exec_cmd(act_env, env_path)
    if instl_packg:
        for pkg in instl_packg:
            if not check_pkg(pkg):
                try:
                    exec_cmd(instl_pkg, pkg)
                except Exception as e:
                    print(e)
            else:
                print("Install package already present", pkg)
    else:
        print("no package present to install in virtual env")
    exec_cmd(list_pkg, req_file)
    if uninstall_pckg:
        for pkg in uninstall_pckg:
            if check_pkg(pkg):
                exec_cmd(uninstl_pkg, pkg)
            else:
                print("package is not present to uninstall :", pkg)
    else:
        print("no package is present to Uninstall from virtual env")
    exec_cmd("pip list --local")
    exec_cmd(list_pkg, req_file)
    if req_file in os.listdir(proj_path):
        rmd_fld = os.path.join(proj_path, req_file)
        os.remove(rmd_fld)
    try:
        shutil.move(req_file, proj_path)
    except Exception as e:
        print(e)
    os.chdir(proj_path)
    print(os.getcwd())
    print("activate process completed...and environment maintenance completed...!!")


def deactivate_env():
    env_path = os.path.join(proj_path, env_nm, "Scripts")
    os.chdir(env_path)
    exec_cmd(deact_env, env_path)
    print(os.getcwd())
    os.chdir(proj_path)
    subprocess.call(["pip", "list", "--local"])
    print(os.getcwd())
    print("deactivate process completed...and environment maintenance completed...!!")


def remove_env():
    print("\nremove environment process starts..")
    try:
        envdir = os.path.join(proj_path, env_nm)
        print(envdir)
        shutil.rmtree(envdir)
    except Exception as e:
        print(e)
    print("remove environment process completed..!!")

if __name__ == "__main__":
    with open('output.txt', 'w') as f, redirect_stdout(f):
        # create_env()
        # manage_env()
        # deactivate_env()
        remove_env()




