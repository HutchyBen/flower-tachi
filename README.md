# flower-tachi
A python tool for importing flower scores into kamaitachi

## How To Use
-  modify config.py script variables to own
    - `TACHI_API_KEY` is optional. outputting to json still exists  
- use -g flag to specify games to import
- use -p flag to specify pages to import
- use -j flag to output json instead of directly importing to tachi

## Example
### Import page 1 to 3 of IIDX single play scores
`python flowertachi.py -g iidx:SP -p 1-3` 
### Import every DDR singles and doubles score
`python flowertachi.py -g ddr:SP ddr:DP`
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

## TODO (in order of priority)
- A fancy TUI
- Maybe support login (I use a hardware key 2fa so :/)
