# DC TTS
   
> back to [main readme](../../README.md)
   
## For **DC_TTS setup** (using pretrained Morgan Freeman model)
   
1. Follow [these steps](../../venv.md) to install virtualenv if you haven't already
    
2. Create virtual environment with requirements:
    
    
    - Create *virtual environment* in your cwd with a specific python version (tested with 3.6.9). This version will need to pre-exist on your system. See [here](../../venv.md) for managing multiple versions with **pyenv**.
       
    ```
    virtualenv -p /home/[USER]/.pyenv/versions/3.6.9/bin/python3.6 dctts-env
    ```
         
    - Activate the venv
    
    ```
    source dctts-env/bin/activate
    ```
   
	- Install requirements
    
    ```
    pip3 install -r requirements.txt
    ```
   
	- Install the older CUDA 10.0 (installs in /usr/local/cuda-10.0)
   
    ```
    sudo apt-get install cuda-toolkit-10-0
    ```
   
    Note: **/usr/local/cuda** is a symlink file now pointing to /usr/local/cuda-10.0 as the default version (feel free to change this)       

	- Deactivate and exit the venv on Linux
    
     ```
	deactivate
	```    
   
3. Clone the dc_tts repo

    ```
    git clone https://github.com/Kyubyong/dc_tts.git
    ```

    Alternate: dctts doesn't have versioned releases. If subsequent commits have broken functionality, you can checkout the commit we used:
   
    ```
    git clone -n https://github.com/Kyubyong/dc_tts.git
    ```
    (The "-n" flag prevents setting the repo's HEAD to latest commit.)
    
    ```
    cd dc_tts
    ```
   
    ```
    git checkout 8b38110875920923343778ff959d01501323765e
    ```
    
    
    

4. Download our [pretrained MF model logdir](https://drive.google.com/file/d/1QftAZ9mNwcVnzZJNhPInAkPP0QCa57Lm/view?usp=sharing) and place in above repo dc_tts/**logdir**.

    - (Model trained on audiobook sample set 747k iterations. If above link expire, see shared package DATA>models>dctts>dctts_audiobook_model_747)

    **Done**

## For Transfer Learning Only (speaker adaption using pretrained model)

This is only required if you're intending to train new voices

1. Copy the following files in dfmotiv/libraries/dctts into the root directory of the cloned https://github.com/Kyubyong/dc_tts.git repo:

    - hyperparams.py
    - data_load.py
    - train.py

2. Download the [pretrained LJ model](https://drive.google.com/file/d/1Uc2E0ZaJ-sjwCLHiR6E0eqN5bz2nPxSE/view?usp=sharing) logdir files (place within a 'logdir' dir in root)
   (Also available in delivered zipped dc_tts/ALT_DATA)

3. Replace with your own wavs and transcript.csv

4. Run prepro and training

- During training, all checkpoints are being retained in dc_tts/logdir/checkpoints.

...
