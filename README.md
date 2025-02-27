# flower-tachi
A python tool for importing flower scores into kamaitachi

## Notice
using recent pages will not work if you don't have any sessions on tachi, make sure to pull all scores first then you can use the recent pages option to only pull new pages from flower

## How To Use
-  modify config.py script variables to own
    - `flower_session` is obtained from cookies on flower website
        - Open inspect element
        - Go to storage/application
        - Go to cookies then https://projectflower.eu
        - Use the value of the flower_session cookie
    - `TACHI_API_KEY` is optional. outputting to json still exists  
- use -g flag to specify games to import
- use -p flag to specify pages to import
- use -j flag to output json instead of directly importing to tachi

## Example
### Import page 1 to 3 of IIDX single play scores
`python flowertachi.py -g iidx:SP -p 1-3` 
### Import all jubeat scores since last session on Tachi 
`python flowertachi.py -g jubeat:Single -p recent`
### Import every DDR singles and doubles score
`python flowertachi.py -g ddr:SP ddr:DP -p all`
> [!CAUTION]
> If you have lots of scores this will send lots of requests to flower. Be nice to them and don't flood them with requests.

## Supported Games
- DanceDanceRevolution (SP/DP)
- GITADORA (Guitar/Drum/Bass)
- jubeat
- pop'n music
- beatmania IIDX (SP/DP)
- Sound Voltex
- MÚSECA
