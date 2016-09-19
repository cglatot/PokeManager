# Pokemon Manager for Pokemon Go

This tool is a CLI tool that uses the [Python API for Pokemon Go available here](https://github.com/rubenvereecken/pokemongo-api), so give them the credit for making this possible.
Also, anything that will work for that API will work here as well.

Feel free to fork this and submit merge requests - I will review them and merge them if they fit with my vision for this tool.

If you have any suggestions, and I like them, I will be happy to look into it - but please don't expect me to be as active as the other developments going on.
Submit an issue with **[Feature]** at the beginning if you would like to make a suggestion.

**Disclaimer**: This is built using an unofficial API. ***All*** of the unofficial APIs stand a risk of getting you banned. So use with caution!

## What does it do?

It does 4 things:

1.  Allows you to view all your Pokemon and their stats (CP, IVs, and Moves)
  1.  It groups / sorts alphabetically, and then by IV%
  2.  It colour codes based on the IV% (Green for >75, Yellow for >50, White for the rest)
2.  Allows you to view how many of each Pokemon you have, as well as how many candies you have for that Pokemon
  1.  It also shows how many you can evolve
  2.  At the bottom of the list it will show you how many "base" Pokemon you can evolve. That is, those Pokemon that are tier 1 evolves only
3.  Allows you to mass transfer Pokemon
  1.  You can set "safe" limits of IV% and CP. This will not transfer anything that is above either of those levels
  2.  **You can set up an exception list of Pokemon to *never* transfer. Look for *exceptions.config* in the root folder. 1 Pokemon per line**
  3.  It will show you how many of that Pokemon is "safe" to transfer, along with their stats
  4.  It will ask how many of the "safe" Pokemon you want to transfer.
  5.  It then shows you the pokemon that will be transferred, and their stats. And asks to confirm if you want to transfer them.
  6.  If specifying certain numbers (lower than the total "safe" Pokemon) it will always transfer the lowest IV% Pokemon first
  7.  You can also choose to transfer duplicate Pokemon. This will keep the most powerful of each type of Pokemon, and transfer the rest (Can also set IV% cutoff)
    1.  This will also ***not** transfer starred Pokemon
4.  Allows you to rename your Pokemon to include their IVs
  1.  Currently it will rename your Pokemon to IV%-ATK/DEF/STA. There is a char limit of 12, so no room for anything else. I chose IV first because you can order by name, thus getting highest IV.
  2.  It allows you to set an IV% limit so it will only rename those Pokemon that are above that limit

## Important Info / Updates

* **Make sure you configure *exceptions.config* in the root folder with the bat file. Pokemon listed here will *never* be transferred. 1 Pokemon name per line.**
* **You can now export the View and Counts to CSV files. They will be in the same directory as the .bat file (or from whichever directory you run the python command)**
* Pokemon names must be in ALL CAPITALS. It uses the API names (easy to look up)
* You can specify **ALL** to transfer all Pokemon below the IV and CP thresholds
* The release and rename functions will take a long time if there are a lot of pokemon. This is to help reduce bot detection by adding delays to requests
* If you have 2FA and it gives you Auth errors, set up an [App Password](https://security.google.com/settings/security/apppasswords).

## How to run it
### Locally, with python
Make sure you have Python and the requirements installed. If you don't have Python installed, search how to do it. **Use Version 2.7.x**. Make sure you have pip as well.

To install the requirements, open a CMD window in the root folder and run:

```pip install -r requirements.txt```

If this gives you an error about not finding pip, please search how to install Python and pip (and make sure python is added to your PATH).

In the root directory there is a file called **PokeManager.bat**. Open it with your favourite editor and you should see this:

```python ".\pogo\demo.py" -a google -u "user@gmail.com" -p "password" -l "lat,lon"```

Replace the email, password, and coordinates (coordinates can also be a location that Google recognises)

If you are on Linux or Max OS, you should replace the line with:

```python "./pogo/demo.py" -a google -u "user@gmail.com" -p "password" -l "lat,lon"```

Run PokeManager.bat. There should be a menu presented to you. Follow along. Don't try to break it - you will.

If you want to use PTC, change `-a google` to `-a ptc`  

### Using Docker
If you have docker installed, you can build this locally using the supplied Dockerfile: 

```docker build .```

Then you can run the image that was just built: 

```docker run --rm -it -e "AUTHTYPE=google" -e "LOGIN=yourlogin@gmail.com" -e "PASSWORD=your-password" -e "STARTINGPOINT=lat, long"  <the image ID that was just made>```
	
or to use a pre-built docker image: 
        
#### Pre-built image: 
```docker run --rm -it -e "AUTHTYPE=google" -e "LOGIN=yourlogin@gmail.com" -e "PASSWORD=your-password" -e "STARTINGPOINT=lat, long" ryebrye/pokemongo-manager:latest```

## Screenshots

### Main Menu

![Main Menu](/media/main_menu3.png?raw=true "Main Menu")

### Viewing Pokemon

![Viewing Pokemon](/media/view_pokemon2.png?raw=true "View Pokemon")

### Viewing Totals of Pokemon

![Counting Pokemon](/media/count_pokemon2.png?raw=true "Count Pokemon")

### Transferring Pokemon

![Transferring Pokemon](/media/transfer_pokemon2.png?raw=true "Transfer Pokemon")

### Renaming Pokemon

![Renaming Pokemon](/media/rename_pokemon.png?raw=true "Rename Pokemon")
