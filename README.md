MapGenerator
===========

Custom dungeon generation algorithm for roguelike games.

All maps are customizable by parameters.

Examples
--------
`#` - wall;
`.` - floor;
`+` - door;
`0` - portal;
`<`, `>` - ladders.

```
                                ##################################              
                    ######      #................................########       
                    #....########.##.###########################.#......#       
                    #..<.+........#....#                       #.#......#       
                    #....##########.>..#                       #.#......#       
            #########....#        #....#                       #........#       
            #.......#....#        #....#                       #.#......#       
           ##+#####.############################################.#......#       
           #......#..............................................##+#.+##       
           #......#.##########+####....................................#        
           #......#.#       #.....######################################        
           #......+.#       #.....#                                             
           ##########       #.....#                                             
                            #.....#                                             
                            #.....#                                             
                            #.....#                                             
                            #######                                             

```
```
 ########                                        #######     #######            
 #......#                                        #.....#     #.....#            
 #......#                                        #.....#     #.....#            
 #......#                                        #.....#     #.....###          
 #......#         #######                        #.....#     #.......#          
 ####.###         #.....#                  #######.....#     #.....#.########   
   #..#           #.....#          ######  #.....#.....#    ########.##.....#   
   #.##           #.....#          #....####.###.##+####    #........##.....### 
   #.#            #.....#       ####.##.#......#....#       #.#########.....+.# 
####.#            ###.######  ###.....+.#......######       #.+....#  #.....#.# 
#....#              #......## #.......#.#......#            ###....#  ###+###.# 
#.#######           ######..# #.#.....#........#              #....#  #...#...# 
#.#.....#                ##.# #.#.....#.#......#              #....#  #.###+### 
#.#.....#    #######    ###.###.#.....#.#......#              ###.#####.#.....# 
#.#.....#    #.....#    #.....#.#######.#####.##                #....##.+.....# 
#.+.....#    #.....#    #.....#.#     #.......#          ###########.####.....# 
###.....#    #.....#    #.....+.#     #########          #.....#.+....+.#.....# 
  ####+##    #.....#    #.....#.#                ######  #.....#.#....#.#.....# 
     #..#    #.....#    #######.#                #....#  #.....#.#....#.###.### 
     ##.#    #.....#     ###....#        #########....#  #.....+.#....#.....#   
  #####+##   ####.##     #......#        #.......#....#  ####################   
  #......######...########.#######      ##+#####......#                         
  #......#.................#.....#      #......####+########                    
  #......+.###..+#########.......#      #......#  #........#                    
  #......#.#.....#       #.......#      #......#  ########.#                    
  #......#.#.....#       #.+.....#   ####......#     #.....#            ######  
  #......#.#.....#       ###.....#   #..+......#     #...<.#         ####....#  
  #.#+####.#.>...#         #######   #.#########     #.....###       #.......#  
  #........#.....################    #.#             #.......# #######.##....#  
  ###.########.#+##.............######+##            ####+##.# #.....#.##....#  
  ###+###    #......###########..#......#             #......# #.....#.##....#  
  #.....#    ######.#....#    ##.#......#      ########.##.### #.......#######  
  #.....#         #......#     #........#      #.....##......# #.....###        
  #.....#         ###....#     ###......#      #.....####....###.....#          
  #.....#           #....#       #......#      #.....####....+.#####+#          
  #.....#           ######       ########      #.....+..#....#.......#          
  #.....#                                      #.....##.+....#########          
  #######                                      ###############                  
                                                                                
```
```
                                                                                
                            ############                                        
                          ###......+...###                                      
                          #......<.###...##                                     
                          #.#......# ###..##                                    
                          #.#......#   ##..#                                    
                          #.#.0....#    ##.#####                                
                          #.#......#     #.....#                                
                          #.########     #.....#                                
                          #......#       #.....#                                
                          ######.#       #.....#                   ########     
   ########                    #.#       #.....#                   #......#     
   #......#                    #.#       #.....#                   #......#     
   #......###           ########.#       #######                   #......#     
   #......+.#           #.+....#.#                                 #......#     
   #......#.#           #.#....#.#                                 #####+##     
   ########.#           #.#....#.#                                     #.#      
          #.#           #.#...0+.#                ##########           #.#      
          #.#           #.########                #.....+..#           #.#      
          #.#           #.#                       #..0..##.#           #.#      
          #.#           #.#          ########     #.....##.#           #.#      
          #.#           #.#          #......#     #..>..##.#           #.#      
          #.#           #.#          #......#     #.....##.#           #.#      
          #.#           #.#          #...0..#     ########.#           #.#      
          #.#  ##########.#          #......#            #.#           #.#      
          #.#  #..........#          #......#            #.#           #.#      
          #.# ##+##########          #......#            #.#           #.#      
          #.# #....#                 ########          ###.##          #.#      
          #.###....#                                   #....#  #########.#      
          #...#....#                                   #....####.+....#..#      
          ###.#....#                                   #....+....+....#.##      
            #.#....#                                   #....+.####......#       
            #.+....#                                   #....###  #....###       
            ########                                   ######    ######         

```

Parameters definition
-----------

`width` - maximum width of dungeon

`height` - maximum height of dungeon

`room_size` - tuple of min and max size of rooms

`rooms_count` - maximum number of rooms in dungeon (actual number of rooms could be less in case there is not enough space)

`transitions_type` - type of transitions between rooms: portals or corridors or both

`portals_percent` - percentage of portals if transitions_type it 'both'

`each_room_transitions` - means that each room have at least one connection

`must_conected` - if it's true, then all rooms should be reachable

`base_connecting` - if it "closest" or "farest" then rooms will be connected with closest/farest neighbor, and "random" is random.

`corridor_curves` - style of corridors. Could be straight (as possible), curve (a lots of turnings). In case of random, this parameter sets randomly to "straight" or "curve" for each corridor

`max_connections_delta` - this parameter needed to delete excess corridors (if it possible, considering "must_connected" parameter)


How to use
-----------

`dungeoun.py` - algorithm module;

`printer.py` - simpliest module for output;

`main.py` - entry point.

To use this module in your project you need only `dungeon.py`.

Example of usage you can see in `main.py`

### Steps:

1. Set up your parameters (it's a dict). All parameters are optional, default values you can find in `dungeon.py`.

2. Call `Generator(params)` from `dungeoun.py`.

3. Then call class function `generate()`

After that you can use next class properties:

`.rooms` - list or rooms

`.corridors` - list of corridors

`.portals` - list of portals

`.exits` - list of tuples (x,y) - coordinates of exits

`.result` - list of rows (lists) with int representation of map (meaning if ints you could see in printer.py)
