# Needed for plotting the results
import matplotlib.pyplot as plt
from board import Blackboard
from utils import new_gif_name


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


def render_episode(fname,experience_buffer):
    configuration = Blackboard().get('configuration')
    enabling = configuration.get('store_gif')
    if enabling:
        fname = configuration.get('output_folder') + new_gif_name()
        fps = configuration.get('fps')
        dpi = configuration.get('dpi')
        interval = configuration.get('interval')
        frames = list(map(lambda x: x['frame'],experience_buffer))
        # Fix frame size
        plt.figure(figsize=(frames[0].shape[1] / dpi, frames[0].shape[0] / dpi), dpi=dpi)
        patch = plt.imshow(frames[0])
        plt.axis('off')

    # Generate animation
    def animate(i):
        patch.set_data(frames[i])

    anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(frames), interval=interval)
    # Salvo l'output come gif
    # anim.save(path + filename, writer='imagemagick', fps=fps)
    # boh,mi da un warning dove dice che utilizza pillow al posto di pillow
    anim.save(path + gifname, writer='Pillow', fps=fps)

    """Salvataggio animazione come video"""
    # Specifica il nome del file video e il percorso di salvataggio
    video_path = 'video.mp4'
    # Specifica la durata di ciascun frame nel video (in secondi)
    frame_duration = 1
    # Salva i frame nel file video utilizzando imageio
    with imageio.get_writer(video_path, mode='I', fps=1 / frame_duration) as writer:
        for frame in frames:
            writer.append_data(frame)
    writer.close()
