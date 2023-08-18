# Needed for plotting the results
import matplotlib.pyplot as plt


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


def store_episode_as_gif_and_video(fname,experience_buffer):
    path = './'
    gifname = fname

    """Salvataggio aniazione come gif"""
    fps = 5   # imposto i frame per secondo
    dpi = 30  # imposto i dots per inch
    interval = 50  # intervallo tra i frames (in ms)

    frames = []
    for experience in experience_buffer:
        frames.append(experience['frame'])

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
