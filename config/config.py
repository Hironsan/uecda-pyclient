# -*- coding: utf-8 -*-
import yaml

FILEIN_DICT = "conf.yaml"

with open(FILEIN_DICT, 'r') as f:
    data = yaml.load(f)
