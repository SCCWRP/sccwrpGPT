#!/bin/bash
sudo echo "" > $(sudo docker inspect --format='{{.LogPath}}' ai-search-tool);
sudo echo "" > $(sudo docker inspect --format='{{.LogPath}}' ai-search-tool-dev);