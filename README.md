# web_ice

## Updates of functions:
1. Zone Clone
2. Add windows and doors to zones ( Known gemotries, dimensions )

## TO RUN
1. Install IDA ICE 4.8 
2. Windows Services Management Tool (system level)  -> start 'IDAMessageBrokerService -> Optional: Startup Type: Automatic
3. Open the project
4. Go to config.py: change APP_PATH and BUILDING_PATH to fit your computer. 
5. Zone Clone and windows add function: (1) BUILDING_PATH : your_project(web_ice)/buildings/ut1.idm
                                        (2) go to runScript.py and run it
                                        (3) You can see the IDA ICE GUI and moniter the automatic constrction in 3D tab directly
