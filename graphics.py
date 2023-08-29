# Needed for plotting the results
from board import Blackboard
from utils import new_gif_name, new_video_name
import imageio # Salva i frame nel file video utilizzando imageio
import matplotlib.pyplot as plt #mi serve per fare il plot delle immagini
from matplotlib import animation #lo tulizzo per generare l'animazione


# Plot reward convergence

def reward_plot(reward_data):
    plot(reward_data,'reward_outfile',"Cumulative reward per episode","Cumulative reward")

def dropoffs_plot(dropdata_data):
    plot(dropdata_data,'dropoffs_outfile',"Failed dropoffs per episode","Failed Dropoffs")

def plot(plotdata, outfilelabel, titlelabel, ylabel):
    configuration = Blackboard().get('configuration')
    file_name = configuration.get('output_folder') + configuration.get(outfilelabel)
    dpi_value = configuration.get('dpi')
    plt.clf()
    plt.title(titlelabel)
    plt.xlabel("Episode")
    plt.ylabel(ylabel)
    plt.plot(plotdata)
    plt.savefig(file_name, format='jpg', dpi=dpi_value)


# definisco le dunzioni che mi permettono di fare il run dell'animazione e di salvarla in formato gif e mp4
def run_animation(experience_buffer):
    """Funzione che lancia l'animazione"""
    time_lag = 0.4  # Delay (in s) between frames
    for experience in experience_buffer:
        # Plot del frame
        plt.imshow(experience['frame'])
        plt.axis('off')
        plt.show(block=False)
        # Pausa animazione
        plt.pause(time_lag)
        # Print console output
        print(f"Episode: {experience['episode']}/{experience_buffer[-1]['episode']}")
        print(f"State: {experience['state']}")
        print(f"Action: {experience['action']}")
        print(f"Reward: {experience['reward']}")
    plt.close()


#todo: extend and fix from configuration for the video


def render_episode(experience_buffer):
    configuration = Blackboard().get('configuration')
    enabling = configuration.get('store_gif')
    if enabling:
        gifname = configuration.get('output_folder') + new_gif_name()
        fps = configuration.get('fps')
        dpi = configuration.get('dpi')
        interval = configuration.get('interval')
        frames = list(map(lambda x: x['frame'],experience_buffer))
        # Fix frame size
        plt.figure(figsize=(frames[0].shape[1] / dpi, frames[0].shape[0] / dpi), dpi=dpi)
        patch = plt.imshow(frames[0])
        plt.axis('off')
        anim = animation.FuncAnimation(plt.gcf(), lambda x: patch.set_data(frames[x]), frames=len(frames), interval=interval)
        anim.save(gifname, writer='Pillow', fps=fps)
        videoname = configuration.get('output_folder') + new_video_name()
        frame_duration = configuration.get('frame_duration')
        with imageio.get_writer(videoname, mode='I', fps=1 / frame_duration) as writer:
            for frame in frames:
                writer.append_data(frame)
        writer.close()
