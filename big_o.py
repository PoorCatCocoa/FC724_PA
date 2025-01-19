import matplotlib.pyplot as plt

methods = ['__init__', 'load_music', 'play_music', 'set_volume', 'skip_forward', 'skip_back', 'update_progress_bar', 'update_time_label', 'update_progress']
complexity = [1, 1, 1, 1, 1, 1, 1, 1, 1]

plt.figure(figsize=(20, 5))
plt.bar(methods, complexity, color='darkblue')
plt.xlabel('Functions')
plt.ylabel('Time Complexity')
plt.title('Big O Analysis for MusicPlayer')
plt.show()