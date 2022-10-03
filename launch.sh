#!/bin/bash
# Copyright 2022 Francisco Pinto-Santos
# See LICENSE for details.

sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install . --upgrade 
sudo python3 -m spacy download xx_ent_wiki_sm
sudo python3 -m spacy download en_core_web_sm
sudo mlgdansk132