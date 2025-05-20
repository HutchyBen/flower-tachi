# flower-tachi
A python tool for importing flower scores into kamaitachi

## Setup
1. Clone this repository or download the zip file from [here](https://github.com/HutchyBen/flower-tachi/archive/refs/heads/main.zip)
2. Install the required packages via the following command `pip install -r requirements.txt`
3. Modify your config.py file
   - Ensure `FLOWER_BASE_URL` is set to the correct URL for your flower instance (for other instances)
   - Set your `FLOWER_SESSION`
     1. Login into flower
     2. Open dev tools
     3. Go to Storage (Firefox) / Application (Chrome) 
     4. Go to Cookies
     5. Use the cookie with the name `flower_session` in the flower domain
   - Set your `TACHI_API_KEY` 
     1. Login into kamaitachi
     2. Click top right profile icon
     3. Go to `My Integrations`
     4. Create a new API key for this tool

## How To Use
> [!CAUTION]
> If you have lots of scores using `-p all` will send lots of requests to flower, and they will not appreciate that so try to only do it once.
### Command line flags
- `-g` or `--games`: Specify the game(s) and playstyle(s) to import.
    - Format: `game_code:playstyle` (e.g., `iidx:SP`, `sdvx:Single`, `gitadora:Gita`).
    - You can specify multiple games by listing them separated by spaces.
    - You can also use `all` to import all games.
- `-p` or `--pages`: Specify the pages to import.
    - Format: `page_number` (e.g., `1`, `2`, `3`) or `recent` to import all recent scores.
    - You can use `all` to import all pages.
    - You can also `recent` to import all scores based on most recent Tachi session. 
    - You can specify a range of pages using a hyphen (e.g., `1-3`).
- `-j` or `--json`: Specify the output format as JSON.
    - This will save the imported scores in a JSON file instead of submitting directly to Tachi.

### Example
#### Import all scores that aren't in Tachi [**RECOMMENDED**]
`python flowertachi.py -g all -p recent`
#### Import page 1 to 3 of IIDX single play scores
`python flowertachi.py -g iidx:SP -p 1-3` 
#### Import all jubeat scores since last session on Tachi 
`python flowertachi.py -g jubeat:Single -p recent`
#### Import every DDR singles and doubles score
`python flowertachi.py -g ddr:SP ddr:DP -p all`

## Issue reporting
I am not the most active arcade player, I don't exactly have the most data to test with so any errors please report them as an issue. 
### What to include in the issue
- The command you used
- The error of the command / kamaitachi error
   - To view errors in kamaitachi go to [this url](https://kamai.tachi.ac/utils/imports/failed) and see if your import is there
   - Please send the error message and Arg 0 input
- A link to your score (if possible) so I can see the score

## Supported Games
- DanceDanceRevolution (SP/DP)
- GITADORA (Guitar/Drum/Bass)
- jubeat
- pop'n music
- beatmania IIDX (SP/DP)
- Sound Voltex
- MÚSECA (Note: MÚSECA Plus currently isn't available in kamaitachi, these scores won't show in kamaitachi)
