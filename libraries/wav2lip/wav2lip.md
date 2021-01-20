
# Wav2Lip | github.com/Rudrabha/Wav2Lip | match a video's lips to a voice
    
- Clone from github https://github.com/Rudrabha/Wav2Lip.git
    
- Description:
  "wav2lip is a package/model that morphs lip movements of talking faces in a videos to match that of a newly supplied video.
  It uses both an accurate pre-trained discriminator as a "lip sync expert" forcing the generator in its GAN setup to produce accurate lip shapes.  It also features a visual quality discriminator to minimize noise and artifacts produced by the generator. This pretrained lip sync expert works quickly on arbitrary faces, so is a suitable option for fast realistic results. "
    
- made "wav2lip_proj" directory with "data" sub-directory to store source mp4 + mp3
    
> back to [main readme](../../README.md)
   
---
      
## For **Wav2Lip setup**
      
1. Follow [these steps](../../venv.md) to install virtualenv if you haven't already
      
2. Create virtual environment with requirements:
    

	- Create *virtual environment* in your cwd with a specific python version (tested with 3.6.9). This version will need to pre-exist on your system. See [here](../../venv.md) for managing multiple versions with **pyenv**.
       
    ```
    virtualenv -p /home/[USER]/.pyenv/versions/3.6.9/bin/python3.6 wav2lip-env
    ```
         
    - Activate the venv
    
    ```
    source /path to your/wav2lip-env/bin/activate
    ```
   
	- Install requirements
    
    ```
    pip3 install -r requirements.txt
    ```
        
	- Deactivate and exit the venv on Linux
    
     ```
	deactivate
	```    
 
3. Install ffmpeg

     ```
	sudo apt-get install ffmpeg
	``` 
    
4. Clone the Wav2lip repo

	```
	git clone https://github.com/Rudrabha/Wav2Lip.git
	```
    
    Alternate: Wav2Lip doesn't have versioned releases. If subsequent commits have broken functionality, you can checkout the commit we used:
    
    ```
    git clone -n https://github.com/Rudrabha/Wav2Lip.git
    ```
    (The "-n" flag prevents setting the repo's HEAD to latest commit.)
    
    ```
    cd Wav2Lip
    ```
   
    ```
    git checkout fda2a15d1437d8a66cdf978e4bedb17652a6276c
    ```
    
5. Download the [face detection model](https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth) and place in the repo **Wav2Lip/face_detection/detection/sfd/s3fd.pth**
    
6. Download [wav2lip_gan](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA?e=n9ljGW) into Wav2Lip/**checkpoints**/**wav2lip_gan.pth**

    **Done**   
    
- ---------------
## Steps to run Wav2Lip individually
    
1. Activate the venv on Linux
    
- Link to wav2lip-env (Or change directory to dfmotiv/libraries/wav2lip and run the below exactly if you created into the library folder)
    
```
source wav2lip-env/bin/activate
```
    
2. Run the lip sync process. Make sure to link to where you have the checkpoint file, your video file and audio file 
    
```
python inference.py --checkpoint_path /...path to../wav2lip_gan.pth --face /..path to../video.mp4 --audio /.. path to ../audio.wav
``` 
    
3. Result in **/Wav2Lip/results**
    
[youtube tutorial](https://www.youtube.com/watch?v=HXag_GIRDi0&ab_channel=NerdyRodent)
