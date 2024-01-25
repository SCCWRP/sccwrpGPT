#!/bin/bash
alias logs='sudo docker container logs -f ai-search-tool';
alias restart='sudo docker container restart ai-search-tool';
alias relog='sudo docker container restart ai-search-tool;sudo docker container logs -f ai-search-tool;';
alias clearlogs='sudo sh -c "echo \"\" > $(docker inspect --format='{{.LogPath}}' ai-search-tool)"';
alias ipython='sudo docker container exec -it ai-search-tool ipython';
