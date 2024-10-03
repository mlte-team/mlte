from PIL import Image
import os
import numpy as np

def compute_rgb_stats(images):
    n = len(images)
    r_avgs = np.zeros(n)
    g_avgs = np.zeros(n)
    b_avgs = np.zeros(n)
    
    for i,image_path in enumerate(images):
        
        image = Image.open(image_path)
        rgb_image = np.array(image.convert('RGB'))
        print(f"{i}: {image_path} - {rgb_image.shape}")
        r_avgs[i] = np.mean(rgb_image[:,:,0])
        b_avgs[i] = np.mean(rgb_image[:,:,1])
        g_avgs[i] = np.mean(rgb_image[:,:,2])
        
    return (r_avgs.mean(), g_avgs.mean(), b_avgs.mean()), (r_avgs.std(),g_avgs.std(),b_avgs.std())

def main(directory):
    files = [directory + image_path for image_path in os.listdir(directory) if image_path.endswith(".jpg")]
    
    (r_avg, g_avg, b_avg),(r_std,g_std,b_std) = compute_rgb_stats(files[:10])
    print(f"RGB stats:\n R={r_avg} ± {r_std}\n G={g_avg} ± {g_std}\n B={b_avg} ± {b_std}\nbased on {len(files)} files")

if __name__ == "__main__":
    directory_path = "media/ox_flower_data/jpg/"
    directory_path = "data/ood/"
    main(directory_path)
