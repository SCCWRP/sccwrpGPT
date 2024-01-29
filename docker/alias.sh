#!/bin/bash
alias logs='sudo docker container logs -f ai-search-tool';
alias restart='sudo docker container restart ai-search-tool';
alias relog='sudo docker container restart ai-search-tool;sudo docker container logs -f ai-search-tool;';
alias clearlogs='sudo sh -c "echo \"\" > $(docker inspect --format='{{.LogPath}}' ai-search-tool)"';
alias ipython='sudo docker container exec -it -w /var/www/sccwrpgpt/testing ai-search-tool ipython';
alias devlogs='sudo docker container logs -f ai-search-tool-dev';
alias devrestart='sudo docker container restart ai-search-tool-dev';
alias devrelog='sudo docker container restart ai-search-tool-dev;sudo docker container logs -f ai-search-tool-dev;';
alias devclearlogs='sudo sh -c "echo \"\" > $(docker inspect --format='{{.LogPath}}' ai-search-tool-dev)"';
alias devipython='sudo docker container exec -it -w /var/www/sccwrpgpt/testing ai-search-tool-dev ipython';
