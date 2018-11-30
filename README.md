# MineZ Bot Rewrite
## MineZ Bot Rewrite has the intention of doing 2 things
- Extending current functionality to be flexible for users to use, and perhaps be used in general purpose ways
- Provide a service current absent from MineZ
## Building this bot for your own server
1. We will be using repl.it. It is possible to host this locally on your own device, but you will need to modify credentials.py and main.py
2. Create an account on repl.it and create a repl https://repl.it/
3. Copy across all files to your Repl
4. Get your Discord token(https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwj1mrKpiP3eAhUvM-wKHeAmDaIQFjAAegQIBBAC&url=https%3A%2F%2Fdiscordapp.com%2Fdevelopers&usg=AOvVaw01ITZetBJJYDSkFaoUknfh) and put it in the respective place in .env
5. Get your Twitter tokens(https://developer.twitter.com/en.html) and put it in the respective place in .env
6. Get your reddit tokens(https://ssl.reddit.com/prefs/apps/) and put them in the respective place in .env
7. Run the Repl.
8. Add your bot to your server by modifying this link with your discord bot client ID(https://discordapp.com/api/oauth2/authorize?client_id=YOUR_DISCORD_CLIENT_ID_HERE&permissions=0&scope=bot)
## Future
- Improve code readability
- Expand and do more thorough bug testing
- Generalise the bot to not be exclusive to MineZ.