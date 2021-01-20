
# venv | creating virtual environments for multiple python and library versions
- dfmotiv requires python3.6.9 to be installed. To maintain your system's current python version and run this system follow the following steps

> back to [main readme](./README.md)

---
## Setup on Linux Ubuntu/Mint with a virtual env
### Install a Python virtual environment
  - [venv](https://docs.python.org/3/tutorial/venv.html) is a self-contained directory tree that contains 
    - a Python installation for a particular version of Python
    - packages and modules that don't come as part of the standard library
    
    Why: Applications sometimes need a specific version of a library, and this version could be in conflict with other applications
         This means it may not be possible for one Python installation to meet the requirements of every application.

    
    **If you don't already have python installed**
    
    ```
    sudo apt-get install python3
    ```
    
    **(Or just install python3.6.9 directly for this system? To be tested)**
    
    
    **See virtualenv package below**  and in addition you will need these packages 
    
    ```
    sudo apt-get install python3-pip
    ```
    
    ```
    sudo apt-get install python3-venv    
    ```
    
  - **pyenv** | manage multiple python installations
    - used homebrew https://docs.brew.sh/Homebrew-on-Linux to install pyenv (adding to homebrew to $PATH in /etc/environment and restarting may be needed)

        ```
        brew install pyenv
        ```
 
	- note: openssl was missing as a standard python package (upon python installation). Installing openssl via brew and the following dev libraries, then passing it to pyenv solved it.
   
	    ```
		sudo apt-get install libssl-dev libffi-dev	    
	    ```

	    ```
		sudo apt-get install libbz2-dev	    
	    ```

	    then run the following to install pyenv
	    
	    ```	    		
    	CFLAGS="-I$(brew --prefix openssl)/include" LDFLAGS="-L$(brew --prefix openssl)/lib" pyenv install -v 3.6.9
	    ```

        
    ---
    ### Optional steps
    note: had to symlink python3 to python executable for pyenv to see system version
   
    ```
    sudo ln -s /usr/bin/python3 /usr/bin/python
    ```
      
    note: may need to have gcc installed prior to installing python version with pyenv, if it isn't already
	
    ```
    sudo apt-get install gcc
    ```
    
  - **virtualenv package**
      Offers a way to install different python versions in a virtual environment (venv) rather than just replacing the "System" version
      
      Note: Still needs the alternate python version installed.
            I already had Python version 3.8.2 already installed (dont have to mess with this)
      

    ```
    sudo pip3 install virtualenv
    ```
    
    **now you are ready to install virtual environments for each system component**
