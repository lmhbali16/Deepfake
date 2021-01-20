# Deep Face Lab (DFL 2.0)
   
> back to [main readme](../../README.md)
 
This utility is for making template videos.
## **For DFL setup**
   
1. Follow [these steps](../../venv.md) to install virtualenv if you haven't already
    
2. Create virtual environment with requirements:
    
    
    - Create *virtual environment* in your cwd with a specific python version (tested with 3.7.9). This version will need to pre-exist on your system. See [here](../../venv.md) for managing multiple versions with **pyenv**.
       
    ```
    virtualenv -p /home/[USER]/.pyenv/versions/3.7.9/bin/python3.7 dfl-env
    ```
         
3. Clone the DFL repos

       - Clone the DFL Linux repo linked in the main DFL repo readme
  
    ```
    git clone https://github.com/nagadit/DeepFaceLab_Linux.git
    ```
    
       - Navigate into the DFL Linux repo
  
    ```
    cd DeepFaceLab_Linux
    ```
    
    - Clone the main DFL repo
   
    ```
    git clone https://github.com/iperov/DeepFaceLab.git
    ```
    
    - Activate the venv
    
    ```
    source dfl-env/bin/activate
    ```
   
	- Install requirements
    
    ```
    pip3 install -r ./DeepFaceLab/requirements-cuda.txt
    ```    
    
       - Deactivate and exit the venv on Linux
         
    ```
    deactivate
    ```  
    
4. Change permissions for the shell scripts
   
       - Navigate into the scripts folder
   
    ```
    cd DeepFaceLab_Linux/scripts
    ```
    
       - Grant execution permission to all the shell scripts
    
    ```
    chmod +x *.sh
    ```
   
    **Done**

## DFL training for new source videos
This is only required if you're intending to train new **source** faces
   
1. Navigate to the scripts folder and prepare the workspace. **Will overwrite any existing data so make sure to backup first or change file/folder names**
   
    ```
    bash ./1_clear_workspace.sh
    ```
   
2. Place your **data_src.mp4** and **data_dst.mp4** videos into the workspace folder
   
3. Extract frames into .png format (recommended 15fps for source video)
   
    ```
    bash ./2_extract_image_from_data_src.sh
    ```
    
    ```
    bash ./3_extract_image_from_data_dst.sh
    ```
    
4. Extract face-sets 
    
    **Select:** 

    - Head
    - Image size = 768 or greater depending on src video resolution
    - Jpeg quality = 100
    
    ```
    bash ./4_data_src_extract_faces_S3FD.sh
    ```
    
    ```
    bash ./5_data_dst_extract_faces_S3FD.sh
    ```
    
    **Optional:** Enhance extracted facesets by increasing their sharpness
    
     ```
    bash ./4.2_data_src_util_faceset_enhance.sh
    ```        
     
    - After completion delete any faces that were extracted incorrectly
        
    
5. Outline X-SEG masks for X-SEG mask training
          
 - Run the following and trace 3-4 head masks for each unique angle and obstruction
      
    ```
    bash ./5_XSeg_data_src_mask_edit.sh
    ```
    
    ```
    bash ./5_XSeg_data_dst_mask_edit.sh
    ```
    
 - Train the X-SEG mask model for around 20k iterations
      
    ```
    bash ./5_XSeg_train.sh
    ```   
    
 - Apply the X-SEG mask model to the source and destination videos
      
    ```
    bash ./5_XSeg_data_src_mask_apply.sh
    ```   
    
    ```
    bash ./5_XSeg_data_dst_mask_apply.sh
    ```   
    
6. Train the deep fake model with SAEHD training
    
    Select this and run for 200k iterations:
   
    - Auto-backup every 1 hr
    - Batch size = 3
    - Eyes priority
    - Auto-encoder dims = 520
    - Encoder dims = 100
    - Decoder dims = 100
    - Head type
    - Resolution = 256
    - Df architecture
    - Gradient Clipping = yes
    
   
    ```
    bash ./6_train_SAEHD.sh
    ```
    
    Perform training for another 50k iterations and enable the following: 
   
    - GAN power = 0.1
   
    Perform training for another 50k iterations and enable the following (keep GAN power enabled): 
   
    - face power = 0.01
   
   
7. Merge the model with the destination video
   
    **Select:** 
   
    - Interactive merger = yes
    - Adjust head scale to liking with 'u' and 'j'
    - 'Shift' + '.>' for applying your changes to all next frames
   
    ```
    bash ./7_merge_SAEHD.sh
    ```
   
8. Output the final mp4 video
   
    ```
    bash ./8_merged_to_mp4.sh
    ```
    
9. View result.mp4 in the workspace folder
   
    
## DFL merging for similar destination videos
This is for applying an already trained model to a new destination video with the same face and angles. **Note:** Additional training may be necessary to better fit the model to the new dst video.
   
1. Place your **data_dst.mp4** videos into the workspace folder
   
2. Extract frames into .png format (recommended 15fps for source video)
   
    ```
    bash ./3_extract_image_from_data_dst.sh
    ```
    
3. Extract face-sets 
    
    **Select:** 
   
    - Head
    - Image size = 768 or greater depending on src video resolution
    - Jpeg quality = 100
   
    ```
    bash ./5_data_dst_extract_faces_S3FD.sh
    ```
    
    - After completion delete any faces that were extracted incorrectly
    
4. Apply X-SEG mask model to destination video
   
    ```
    bash ./5_XSeg_data_dst_mask_apply.sh
    ```   
   
5. **Optional:** Further train the deep fake model with SAEHD training. See "DFL training for new source videos" Step 6.
   
    ```
    bash ./6_train_SAEHD.sh
    ```
   
7. Merge the model with the destination video
    
    **Select:** 
    
    - Interactive merger = yes
    - Adjust head scale to liking with 'u' and 'j'
    - 'Shift' + '.>' for applying your changes to all next frames
    
    ```
    bash ./7_merge_SAEHD.sh
    ```
    
8. Output the final mp4 video
    
    ```
    bash ./8_merged_to_mp4.sh
    ```
    
9. View result.mp4 in the workspace folder
   
...
