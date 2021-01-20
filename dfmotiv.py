
import os
import sys
import yaml
import subprocess
import glob
import shutil
import argparse
import errno


VALID_EXT = ["mp4", "wav"]
SPEECH_FILE = "./src/speech.txt"
PATHS_FILE = "./paths.yml"

outaudio = "output.wav"
outvideo = "output.mp4"

# temp hardcoded
default_tempate = "template.mp4"

# read paths 
with open(PATHS_FILE) as f:
    paths = yaml.safe_load(f)

def main(args):
    """
    
    dfmotiv main
    
    text to voice synthesis: output.wav
    morph mouth shapes in template.mp4 with output.wav in sync: output.mp4

    """
    outaudio_path = None
    video_out = None
    
    if args.outpath:
        out_tokens = os.path.splitext(args.outpath)
        out_ext = out_tokens[-1].lower().replace(".", "") if len(out_tokens) == 2 else ""
        
        # Validate ext
        if out_ext not in VALID_EXT:
            valid_ext_str = ", ".join(VALID_EXT)
            raise ValueError("\"{}\" isn't support for output. Try these: {}".format(out_ext, valid_ext_str))
        
        if out_ext == "wav":
            outaudio_path = args.outpath
            args.audio_only = True
        elif out_ext == "mp4":
            video_out = args.outpath

    # ---------------------
    # dctts exec in venv
    # ---------------------
    
    # speech text
    speech_text = args.text
    if not speech_text:
        
        # No speech txt provided via cmdline or file
        if not os.path.isfile(SPEECH_FILE):
            raise FileNotFoundError(errno.ENOENT, "Please provide speech text via cmd line -t flag or speech file", SPEECH_FILE)
        
        with open(SPEECH_FILE, 'r') as f:
            speech_text = f.readline()

    rootdir = os.path.dirname(os.path.realpath(__file__))
    if not outaudio_path:
        outaudio_path = os.path.join(rootdir, "out", outaudio)

    subprocess_venv_run("dctts", speech_text, outaudio_path)
    
    if args.audio_only:
        print("Exported audio %s" % outaudio_path)
        return

    # ---------------------
    # wav2lip exec in venv
    # ---------------------
    # video template
    if args.video_in:
        if args.video_in == os.path.basename(args.video_in):
            video_in = os.path.join(rootdir, "src", args.video_in)
        else:
            video_in = args.video_in
    else:
        video_in = os.path.join(rootdir, "src", default_tempate)

    # video out path
    if not video_out:
        video_out = os.path.join(rootdir, "out", outvideo)
    
    wav2lip_cp = os.path.join(paths["wav2lip"]["pkg"], "checkpoints", "wav2lip_gan.pth")

    args = [
        '--checkpoint_path', wav2lip_cp,
        '--face', video_in,
        '--audio', outaudio_path,
        '--outfile', video_out
    ]
    subprocess_venv_run("wav2lip", *args, runfile="inference.py")
    print("Exported video: %s" % video_out)


def subprocess_venv_run(pkg_key, *args, runfile="run.py"):
    """
    lib runner exec in venv
    e.g subprocess_venv_run("wav2lip", audio_in, video_in, out_video)

    Args:
        pkg_key (str): "wav2lip" | "dctts" (see libraries/ and paths.yml)
        *args: runfile cmd args
        runfile (str, optional): file name to exec in package. Defaults to "run.py".

    """ 
    

    pkg_path = paths[pkg_key]["pkg"]
    venv_path = paths[pkg_key]["venv"]

    # Paths to venv python and run.py
    venv_python = os.path.join(venv_path, "bin", "python3")
    runfile_path = os.path.join(pkg_path, runfile)
        
    modified_files = glob.glob("./libraries/%s/*.py" % pkg_key)
    for filepath in modified_files:
        filename = os.path.split(filepath)[-1]
        print(filepath, os.path.join(pkg_path, filename))
        shutil.copy(filepath, os.path.join(paths["dctts"]["pkg"], filename))
    
    # Spawn voice synthesis process 
    run_args = [arg for arg in args]
    p = subprocess.Popen([venv_python, runfile_path] + run_args, 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=pkg_path)
    out, err = p.communicate()
    # Note: cwd=pkg_path because too many file reads within are relative (wernt being found)
                    
    print(out.decode('utf-8'))
    if p.returncode !=0:
        raise Exception("An error has been thrown within subprocess:\n{}".format(err.decode('utf-8')))




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='dfmotiv: deepfake and voice sythesis tool')
    parser.add_argument('-t', '--text', type=str, 
					help='text string to become speech', 
                    required=False)
    parser.add_argument('-a', '--audio-only', 
					help='synthesize audio only', 
                    required=False, action="store_true")
    parser.add_argument('-o', '--outpath', 
					help='Output path to mp4 or wav', 
                    required=False)
    parser.add_argument('-v', '--video-in', 
					help="""Template video containing a face to be morphed and synced to new audio.
                    Default is dfmotiv/src/template.mp4. 
                    dfmotiv/src/* will be searched if only a filename is provided
                    """,
                    required=False)
    main(parser.parse_args())