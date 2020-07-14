import json
import os
import re

import gcp_secrets_fetcher.secret_fetcher as secret_fetcher

secrets_client = secret_fetcher.get_secret_manager_client()


def env(key, default, cast=str):
    return cast(os.environ.get(key, default))


# Webserver configuration #
###########################

# gunicorn config
bind = '0.0.0.0:5000'
debug = env('PULLSBURY_GUNICORN_DEBUG', True, bool)
loglevel = env('PULLSBURY_GUNICORN_LOGLEVEL', 'debug')

# Config file for logging
LOGGING_CONFIG = './logging.ini'

# General project configuration #
#################################

# Slack settings
SLACK_AUTH_TOKEN = secret_fetcher.fetch_secret(
    secrets_client,
    'freshbooks-builds-secrets',
    'pullsbury-gitboy-slack-token',
    'latest'
)

SLACK_ICON = 'https://i.imgur.com/oEL0h26.jpg'
HAPPY_SLACK_EMOJIS = [
    "boom",
    "doge",
    "wow",
    "star_mario",
    "ninja",
    "hero",
    "high5",
    "eli",
    "1up_mario",
    "fire",
    "awesome",
    "carlton",
    "excited_bunny",
    "dancing-penguin",
    "yess",
    "leaf",
    "love",
    "parrot",
    "party",
    "tada",
    "pika_dance",
    "yay",
    "fidget_spinner",
    "ohyah_dance",
    "pokeball",
    "dancing-wyatt",
    "at_jakewow",
    "siren",
    "sparkles",
    "ok_hand",
    "sb_dance",
    "bananadance",
    "corgi-wait",
    "fingerguns-op-right",
    "partysheep"
]

SLACK_CUSTOM_EMOJI_MAPPING = {
    "alexbaizeau": "flag-fr",
    "alexvermeulen": "eli",
    "amcintosh": "amcintosh",
    "anton": "antonrainbow",
    "asodhi": "fireball",
    "calvin-fb": "calvin",
    "ctroup": "ctroup",
    "ellovell": "parrot_doge",
    "FreshTheresa": "pika_dance",
    "goakham": "eyeball",
    "hc04": "harris2",
    "jessy": "bathroom",
    "jeffsawatzky": "jeffslide",
    "k-fish": "cool-doge",
    "larumugam": "snap",
    "MatthewSBarnes": "bankrovers",
    "natashad": "natashad",
    "nwoodger": "pokeball",
    "rkachooei": "sb_dance",
    "Sergiyko16": "man_climbing",
    "tabiodun": "man-gesturing-no::skin-tone-4",
    "Khan-Saad": "at_jakewow",
    "a-rob": "waffles",
    "David": "pika_dance",
    "laurawong": "corgibutt"
}

TEAMS = {
    "6ix": {
        "AntonNguyen": {
            "slack": "anton"
        },
        "jeffsawatzky": {
            "slack": "jsawatzky"
        },
        "pranjal-natu": {
            "slack": "Pranjal Natu"
        },
        "amcintosh": {
            "slack": "amcintosh"
        },
        "natashad": {
            "slack": "natasha"
        },
        "nicholasyee": {
            "slack": "Dr. Nick"
        },
        "RyanMarr": {
            "slack": "Ryan"
        },
        "ngalandefb": {
            "slack": "Nachiket"
        },
        "abmohan": {
            "slack": "Ashwin Balamohan"
        }
    },
    "alchemy": {
        "laurawong": {
            "slack": "lauraw"
        },
        "eduenriquez": {
            "slack": "eduzen"
        },
        "mishok13": {
            "slack": "mishok13"
        },
        "romulocollopy": {
            "slack": "roms"
        },
        "matematik7": {
            "slack": "Domen Ipavec"
        },
        "codado-nl": {
            "slack": "Damir Alagic"
        },
        "hc04": {
            "slack": "harris"
        },
        "k-tran": {
            "slack": "kiet"
        },
        "jkwill87": {
            "slack": "jessy"
        },
        "MatthewSBarnes": {
            "slack": "mattiebarnes"
        },
        "maxlvl": {
            "slack": "maxvl"
        },
        "chandnap": {
            "slack": "Prerna Chandna"
        },
        "rdeguy": {
            "slack": "rdeguy"
        },
        "rchrdschfr": {
            "slack": "richard"
        },
        "yulia-che": {
            "slack": "yulia"
        },
        "mikanchu": {
            "slack": "Elena He"
        }
    },
    "billing-core-team": {
        "dygcao": {
            "slack": "gerard"
        },
        "AnthonyRobertson17": {
            "slack": "a-rob"
        },
        "hsungje": {
            "slack": "David"
        },
        "CobiOneCanobi": {
            "slack": "cobi"
        }
    },
    "catalyst": {
        "g--": {
            "slack": "goakham"
        },
        "mayurpatel": {
            "slack": "mayur"
        },
        "mmazer": {
            "slack": "mmazer"
        },
        "smetcalfe-fb": {
            "slack": "smetcalfe"
        },
        "tobioboye": {
            "slack": "togunbiyi"
        },
        "drone115b": {
            "slack": "Mayur"
        },
        "sfreudenthaler": {
            "slack": "Steve Freudenthaler"
        }
    },
    "dxp-spam": {
        "jali-clarke": {
            "slack": "Jinnah Ali-Clarke"
        }
    },
    "team-hugs": {
        "mmazer": {
            "slack": "mmazer"
        },
        "tobioboye": {
            "slack": "togunbiyi"
        },
        "patrickmariglia": {
            "slack": "Patrick Mariglia"
        }
    },
    "team-sas": {
        "kuntalFreshBooks": {
            "slack": "Kuntal"
        },
        "dtse19": {
            "slack": "David Tse"
        }
    },
    "groot": {
        "brentsmyth": {
            "slack": "brentsmyth"
        },
        "spatel": {
            "slack": "Sameer Patel"
        }
    },
    "london-underground": {
        "calvin-fb": {
            "slack": "calvin"
        },
        "rkachooei": {
            "slack": "roya"
        },
        "stevepentland": {
            "slack": "StevePentland"
        },
        "parulraheja98": {
            "slack": "Parul Raheja"
        },
        "rahmed-freshbooks": {
            "slack": "Rashid Ahmed"
        },
        "nickpyren": {
            "slack": "Nicholas Pyren"
        },
        "vibhorfb": {
            "slack": "Vibhor Nikhra"
        },
        "DanielChanJA": {
            "slack": "Daniel Chan"
        }
    },
    "payments": {
        "Onjrew": {
            "slack": "aferguson"
        },
        "asodhi": {
            "slack": "asodhi"
        },
        "alexvermeulen": {
            "slack": "avermeulen"
        },
        "dharmesh-dhakan": {
            "slack": "ddhakan"
        },
        "davidristovski": {
            "slack": "DavidR"
        },
        "DeanWay": {
            "slack": "dway"
        },
        "ellovell": {
            "slack": "elovell"
        },
        "murrayrush": {
            "slack": "mrush"
        },
        "tabiodun": {
            "slack": "tabiodun"
        },
        "FreshTheresa": {
            "slack": "theresa"
        },
        "Sergiyko16": {
            "slack": "solshanetskyi"
        },
        "jleefresh": {
            "slack": "jale"
        }
    },
    "amfm-team": {
        "dlinley": {
            "slack": "dlinley"
        },
        "ionut998": {
            "slack": "alexandru"
        },
        "seanmoon80": {
            "slack": "Sean Moon"
        },
        "TusconDanksman": {
            "slack": "jstinson"
        }
    },
    "tng": {
        "aabzhanova": {
            "slack": "aabzhanova"
        },
        "Khan-Saad": {
            "slack": "Saad Khan"
        },
        "dannifreshbooks": {
            "slack": "Danni"
        },
        "k-fish": {
            "slack": "kfisher"
        },
        "neilanderson": {
            "slack": "nanderson"
        },
        "nwoodger": {
            "slack": "nwoodger"
        }
    }
}

# List of repos to not notify
REPO_BLACKLIST = [
    "ops/puppet-private",
    "ops/puppet-pci",
    "ops/puppet-pci-secrets"
]

# json serialize all the things :(

_var_regex = re.compile(r"^[A-Z]([A-Z_])*$")
module_vars = globals().copy()

for var_name, var_value in module_vars.items():
    if _var_regex.match(var_name) and (isinstance(var_value, list) or isinstance(var_value, dict)):
        globals()[var_name] = json.dumps(var_value)
