import pandas as pd
import numpy as np
from os import path


def load_data(data_folder: str):
    """Loads all garden data results and taxonomy categories."""
    df_results = pd.read_csv(path.join(data_folder, 'FlowerModelv1_TestSetResults.csv'))
    df_results.drop(columns = ['Unnamed: 0'], inplace = True)
    df_results.rename(columns = {'label':'Label'}, inplace = True)
    df_results.head()

    #load the taxonomic data
    df_labels = pd.read_csv(path.join(data_folder, 'OxfordFlowerLabels.csv'), header = 1)
    df_labels.drop(columns = ['Phylum', 'Class'], inplace = True)
    df_labels.rename(columns = {'Phylum.1':'Phylum'}, inplace = True)
    df_labels.drop([0],inplace=True)
    #df_labels['Common Name'] = df_labels['Common Name'].str.strip()
    df_labels['Label Name'] = df_labels['Common Name'].replace(' ','_', regex=True)
    df_labels.head()

    label_dict = {0: '_mexican_aster', 1: 'alpine_sea_holly', 2: 'anthurium', 3: 'artichoke', 4: 'arum_lily', 5: 'azalea', 6: 'ball_moss', 7: 'ballon_flower', 8: 'barberton_daisy', 9: 'bearded_iris', 10: 'bee_balm', 11: 'bird_of_paradise', 12: 'bishop_of_llandaf_dahlia', 13: 'black-eyed_susan', 14: 'blackberry_lily', 15: 'blanket_flower', 16: 'bolero_deep_blue', 17: 'bougainvillea', 18: 'bromelia', 19: 'buttercup', 20: 'california_poppy', 21: 'camellia', 22: 'canna_lily', 23: 'canterbury_bells', 24: 'cape_flower', 25: 'carnation', 26: 'cattleya', 27: 'cautleya_spicata', 28: 'clematis', 29: 'coltsfoot', 30: 'columbine', 31: 'common_dandelion', 32: 'corn_poppy', 33: 'cyclamen', 34: 'daffodil', 35: 'dahlia', 36: 'desert_rose', 37: 'english_marigold', 38: 'fire_lily', 39: 'foxglove', 40: 'frangipani', 41: 'fritillary', 42: 'garden_phlox', 43: 'gaura', 44: 'gazania', 45: 'geranium', 46: 'globe_flower', 47: 'globe_thistle', 48: 'grape_hyacinth', 49: 'great_masterwort', 50: 'hard-leaved_pocket_orchid', 51: 'hibiscus', 52: 'hippesatrum', 53: 'japanese_anemone', 54: 'king_protea', 55: 'lenten_rose', 56: 'lotus', 57: 'love_in_the_mist', 58: 'magnolia', 59: 'mallow', 60: 'marigold', 61: 'mexican_petunia', 62: 'monkshood', 63: 'moon_orchild', 64: 'morning_glory', 65: 'osteospermum', 66: 'oxeye_daisy', 67: 'passion_flower', 68: 'pelargonium', 69: 'peruvian_lily', 70: 'petunia', 71: 'pincushion_flower', 72: 'poinsettia', 73: 'primrose', 74: 'primula', 75: 'prince_of_whales_feather', 76: 'purple_coneflower', 77: 'red_ginger', 78: 'rose', 79: 'siam_tulip', 80: 'silverbush', 81: 'snapdragon', 82: 'spear_thistle', 83: 'spring_crocus', 84: 'stemless_gentain', 85: 'sunflower', 86: 'swear_pea', 87: 'sweet_william', 88: 'sword_lily', 89: 'thorn_apple', 90: 'tiger_lily', 91: 'tithonia_(incorrectly_labeled_as_orange_dahlia)', 92: 'toad_lily', 93: 'tree_mallow', 94: 'tree_poppy', 95: 'trumpet_creeper', 96: 'wallflower', 97: 'water_lily', 98: 'watercress', 99: 'wild_pansy', 100: 'windflower', 101: 'yellow_iris'}
    df_dict = pd.DataFrame.from_dict( {'Label':list(label_dict),'Label Name':label_dict.values()} )
    df_dict.head()

    df_info = df_labels.merge(df_dict, how = 'outer', left_on = 'Label Name', right_on = 'Label Name')
    df_info['Clade1'].fillna('None',inplace = True)
    df_info['Clade2'].fillna('None',inplace = True)
    df_info['Clade 3'].fillna('None',inplace = True)
    df_info['Subfamily'].fillna('None',inplace = True)
    df_info['Genus'].fillna('None',inplace = True)
    df_info['Risk'].fillna('None',inplace = True)
    df_info

    print(len(df_info), len(df_labels), len(df_dict))

    #merge the info w the model results
    df_all = df_results.merge(df_info, left_on = 'Label', right_on = 'Label')
    df_all
    return df_info, df_all


def split_data(df_info, df_all):
    """Splits the data into 3 different populations to evaluate them."""
    df_gardenpop = df_info.copy()
    df_gardenpop['Population1'] = (np.around(np.random.dirichlet
                            (np.ones(df_gardenpop.shape[0]),size=1)[0],
                            decimals = 3) *1000).astype(int)
    df_gardenpop['Population2'] = (np.around(np.random.dirichlet
                            (np.ones(df_gardenpop.shape[0]),size=1)[0],
                            decimals = 3) *1000).astype(int)
    df_gardenpop['Population3'] = (np.around(np.random.dirichlet
                            (np.ones(df_gardenpop.shape[0]),size=1)[0],
                            decimals = 3) *1000).astype(int)
    df_gardenpop

    #build populations from test data set that match the garden compositions
    from random import choices

    #build 3 gardens with populations of 1000.
    pop_names = ['Population1', 'Population2', 'Population3']
    gardenpops = np.zeros( (3,1000), int)
    gardenmems = np.zeros( (3,1000), int)

    for j in range(1000):
        for i in range(len(df_gardenpop)):
            my_flower = df_gardenpop.iloc[i]['Common Name']
        
            for g in range(3):
                n_choices = df_gardenpop.iloc[i][pop_names[g]]
                my_choices = df_all[df_all['Common Name'] == my_flower]['model correct'].to_list()
                my_selection = choices(my_choices, k=n_choices)
            
                gardenpops[g][j] += sum(my_selection)
                gardenmems[g][j] += len(my_selection)

    gardenpops

    return gardenpops, gardenmems


def calculate_model_performance_acc(gardenpops, gardenmems):
    """Get accucray of models across the garden populations"""
    gardenacc = np.zeros( (3,1000), float)
    for i in range (1000):
        for g in range(3):
            gardenacc[g][i] = gardenpops[g][i]/gardenmems[g][i]
    gardenacc

    model_performance_acc = []
    for g in range(3):
        avg = round(np.average(gardenacc[g][:]),3)
        std = round(np.std(gardenacc[g][:]),3)
        min = round(np.amin(gardenacc[g][:]),3)
        max = round(np.amax(gardenacc[g][:]),3)
        model_performance_acc.append(round(avg,3))
        
        print("%1d %1.3f %1.3f %1.3f %1.3f" % (g, avg, std, min, max))

    return model_performance_acc
