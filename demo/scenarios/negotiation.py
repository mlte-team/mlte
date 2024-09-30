from mlte.model.shared import (
    DataClassification,
    DataDescriptor,
    FieldDescriptor,
    LabelDescriptor,
    MetricDescriptor,
    ModelDescriptor,
    ModelDevelopmentDescriptor,
    ModelInterfaceDescriptor,
    ModelIODescriptor,
    ModelProductionDescriptor,
    ModelResourcesDescriptor,
    QASDescriptor,
)
from mlte.negotiation.artifact import NegotiationCard
from mlte.negotiation.model import (
    GoalDescriptor,
    ProblemType,
    RiskDescriptor,
    SystemDescriptor,
)

goals = [
    GoalDescriptor(
        description="The model should perform well.",
        metrics=[
            MetricDescriptor(
                description="accuracy",
                baseline="Better than random chance.",
            )
        ],
    )
]


label_dict = {
    0: "_mexican_aster",
    1: "alpine_sea_holly",
    2: "anthurium",
    3: "artichoke",
    4: "arum_lily",
    5: "azalea",
    6: "ball_moss",
    7: "ballon_flower",
    8: "barberton_daisy",
    9: "bearded_iris",
    10: "bee_balm",
    11: "bird_of_paradise",
    12: "bishop_of_llandaf_dahlia",
    13: "black-eyed_susan",
    14: "blackberry_lily",
    15: "blanket_flower",
    16: "bolero_deep_blue",
    17: "bougainvillea",
    18: "bromelia",
    19: "buttercup",
    20: "california_poppy",
    21: "camellia",
    22: "canna_lily",
    23: "canterbury_bells",
    24: "cape_flower",
    25: "carnation",
    26: "cattleya",
    27: "cautleya_spicata",
    28: "clematis",
    29: "coltsfoot",
    30: "columbine",
    31: "common_dandelion",
    32: "corn_poppy",
    33: "cyclamen",
    34: "daffodil",
    35: "dahlia",
    36: "desert_rose",
    37: "english_marigold",
    38: "fire_lily",
    39: "foxglove",
    40: "frangipani",
    41: "fritillary",
    42: "garden_phlox",
    43: "gaura",
    44: "gazania",
    45: "geranium",
    46: "globe_flower",
    47: "globe_thistle",
    48: "grape_hyacinth",
    49: "great_masterwort",
    50: "hard-leaved_pocket_orchid",
    51: "hibiscus",
    52: "hippesatrum",
    53: "japanese_anemone",
    54: "king_protea",
    55: "lenten_rose",
    56: "lotus",
    57: "love_in_the_mist",
    58: "magnolia",
    59: "mallow",
    60: "marigold",
    61: "mexican_petunia",
    62: "monkshood",
    63: "moon_orchild",
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
    75: "prince_of_whales_feather",
    76: "purple_coneflower",
    77: "red_ginger",
    78: "rose",
    79: "siam_tulip",
    80: "silverbush",
    81: "snapdragon",
    82: "spear_thistle",
    83: "spring_crocus",
    84: "stemless_gentain",
    85: "sunflower",
    86: "swear_pea",
    87: "sweet_william",
    88: "sword_lily",
    89: "thorn_apple",
    90: "tiger_lily",
    91: "tithonia_(incorrectly_labeled_as_orange_dahlia)",
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

data = [
    DataDescriptor(
        description="Oxford flower dataset.",
        classification=DataClassification.UNCLASSIFIED,
        access="None",
        labeling_method="by hand",
        fields=[
            FieldDescriptor(
                name="filename",
                description="path to flower image.",
                type="string to png file",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Kingdom",
                description="The second highest taxonomic rank.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Phylum",
                description="The taxonomic rank below kingdom and above Clade 1.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Clade1",
                description="The taxonomic rank below Phylum and above Clade 2.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Clade2",
                description="The taxonomic rank below Clade 1 and above Clade 3.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Clade3",
                description="The taxonomic rank below Clade 2 and above Order.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Order",
                description="The taxonomic rank below Clade 3 and above Family.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Family",
                description="The taxonomic rank below Order and above Subfamily.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Subfamily",
                description="The taxonomic rank below Family and above Genus.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Genus",
                description="The taxonomic rank below Subfamily and above Species.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Common Name",
                description="Image of flower including background.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Other Name",
                description="Image of flower including background.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Risk",
                description="Image of flower including background.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
            FieldDescriptor(
                name="Label Name",
                description="Image Label.",
                type="string",
                expected_values="N/A",
                missing_values="N/A",
                special_values="N/A",
            ),
        ],
        labels=[
            LabelDescriptor(description=label_dict[k], percent=0.0)
            for k in label_dict
        ],
        policies="N/A",
        rights="N/A",
        source="https://www.robots.ox.ac.uk/~vgg/data/flowers/102/",
    )
]


risks = RiskDescriptor(
    fp="The wrong type of flower is identified.",
    fn="The flower is not identified.",
    other="N/A",
)


# card = NegotiationCard(
#     system=[],
#     data=[],
#     model=[],
#     qas=[]
# )

card = NegotiationCard(
    system=SystemDescriptor(
        goals=goals,
        problem_type=ProblemType.CLASSIFICATION,
        task="Flower Classification",
        usage_context="A handheld flower identification device.",
        risks=RiskDescriptor(
            fp="The wrong type of flower is identified.",
            fn="The flower is not identified.",
            other="N/A",
        ),
    ),
    data=data,
    model=ModelDescriptor(
        development=ModelDevelopmentDescriptor(
            resources=ModelResourcesDescriptor(
                cpu="1", gpu="0", memory="6MiB", storage="2KiB"
            )
        ),
        production=ModelProductionDescriptor(
            deployment_platform="local server",
            capability_deployment_mechanism="API",
            interface=ModelInterfaceDescriptor(
                input=ModelIODescriptor(
                    name="i1", description="description", type="Vector[150]"
                ),
                output=ModelIODescriptor(
                    name="o1", description="description", type="Vector[3]"
                ),
            ),
            resources=ModelResourcesDescriptor(
                cpu="1",
                gpu="0",
                memory="6MiB",
                storage="2KiB",
            ),
        ),
    ),
    qas=[],
)
