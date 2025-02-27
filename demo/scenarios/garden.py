from os import path

import pandas as pd

# set up a data label dictionary to switch between data label number and english name
label_dict = {
    0: "alpine_sea_holly",
    1: "anthurium",
    2: "artichoke",
    3: "arum_lily",
    4: "azalea",
    5: "ball_moss",
    6: "balloon_flower",
    7: "barberton_daisy",
    8: "bearded_iris",
    9: "bee_balm",
    10: "bird_of_paradise",
    11: "bishop_of_llandaf_dahlia",
    12: "black-eyed_susan",
    13: "blackberry_lily",
    14: "blanket_flower",
    15: "bolero_deep_blue",
    16: "bougainvillea",
    17: "bromelia",
    18: "buttercup",
    19: "california_poppy",
    20: "camellia",
    21: "canna_lily",
    22: "canterbury_bells",
    23: "cape_flower",
    24: "carnation",
    25: "cattleya",
    26: "cautleya_spicata",
    27: "clematis",
    28: "coltsfoot",
    29: "columbine",
    30: "common_dandelion",
    31: "corn_poppy",
    32: "cyclamen",
    33: "daffodil",
    34: "dahlia",
    35: "desert_rose",
    36: "english_marigold",
    37: "fire_lily",
    38: "foxglove",
    39: "frangipani",
    40: "fritillary",
    41: "garden_phlox",
    42: "gaura",
    43: "gazania",
    44: "geranium",
    45: "globe_flower",
    46: "globe_thistle",
    47: "grape_hyacinth",
    48: "great_masterwort",
    49: "hard-leaved_pocket_orchid",
    50: "hibiscus",
    51: "hippeastrum",
    52: "japanese_anemone",
    53: "king_protea",
    54: "lenten_rose",
    55: "lotus",
    56: "love_in_the_mist",
    57: "magnolia",
    58: "mallow",
    59: "marigold",
    60: "mexican_aster",
    61: "mexican_petunia",
    62: "monkshood",
    63: "moon_orchid",
    64: "morning_glory",
    65: "osteospermum",
    66: "oxeye_daisy",
    67: "passion_flower",
    68: "pelargonium",
    69: "peruvian_lily",
    70: "petunia",
    71: "pincushion_flower",
    72: "poinsettia",
    73: "primrose",
    74: "primula",
    75: "prince_of_wales_feather",
    76: "purple_coneflower",
    77: "red_ginger",
    78: "rose",
    79: "siam_tulip",
    80: "silverbush",
    81: "snapdragon",
    82: "spear_thistle",
    83: "spring_crocus",
    84: "stemless_gentian",
    85: "sunflower",
    86: "sweet_pea",
    87: "sweet_william",
    88: "sword_lily",
    89: "thorn_apple",
    90: "tiger_lily",
    91: "tithonia",
    92: "toad_lily",
    93: "tree_mallow",
    94: "tree_poppy",
    95: "trumpet_creeper",
    96: "wallflower",
    97: "water_lily",
    98: "watercress",
    99: "wild_pansy",
    100: "windflower",
    101: "yellow_iris",
}


def load_base_results(data_folder: str, test_filename: str) -> pd.DataFrame:
    df_results = pd.read_csv(path.join(data_folder, test_filename))
    df_results.drop(columns=["Unnamed: 0"], inplace=True)
    return df_results


def load_taxonomy(data_folder: str) -> pd.DataFrame:
    """Loads taxonomy info about the flowers and returns a dict with it."""
    df_labels = pd.read_csv(
        path.join(data_folder, "OxfordFlowerLabels.csv"), header=0
    )
    # print(df_labels.head())
    df_labels.drop(columns=["Phylum", "Class"], inplace=True)
    df_labels.rename(columns={"Phylum.1": "Phylum"}, inplace=True)
    # df_labels.drop([0], inplace=True)
    # df_labels['Common Name'] = df_labels['Common Name'].str.strip()
    df_labels["Label Name"] = df_labels["Common Name"].replace(
        " ", "_", regex=True
    )
    #print(df_labels)

    df_dict = pd.DataFrame.from_dict(
        {"Label": list(label_dict), "Label Name": label_dict.values()}
    )
    df_dict.head()

    # fill in missing data metadata
    df_info = df_labels.merge(
        df_dict, how="outer", left_on="Label Name", right_on="Label Name"
    )
    df_info.fillna({"Clade1": "None"}, inplace=True)
    df_info.fillna({"Clade2": "None"}, inplace=True)
    df_info.fillna({"Clade3": "None"}, inplace=True)
    df_info.fillna({"Subfamily": "None"}, inplace=True)
    df_info.fillna({"Genus": "None"}, inplace=True)
    df_info.fillna({"Risk": "None"}, inplace=True)

    df_info
    print(len(df_info), len(df_labels), len(df_dict))

    return df_info


def merge_taxonomy_with_results(
    df_results: pd.DataFrame,
    df_info: pd.DataFrame,
    left_on: str = "Label",
    right_on: str = "Label",
) -> pd.DataFrame:
    """Merge results with taxonomy."""
    df_all = df_results.merge(df_info, left_on=left_on, right_on=right_on)
    df_all
    return df_all
