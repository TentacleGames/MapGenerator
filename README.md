MapGenerator
===========

Customizable dungeon generation algorithm for roguelike games.

All maps are customizable by parameters, described just below these exmaples.

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

`rooms_count` - maximum number of rooms in dungeon (if there's not enough space, the actual number of rooms could be less than)

`transitions_type` - type of transitions between rooms: portals or corridors or both

`portals_percent` - percentage of portals if transitions_type is 'both'

`each_room_transitions` - means that each room have at least one connection to another room

`are_connected` - if it's true, then all rooms should be reachable

`base_connecting` - if it's "closest" or "farest" then rooms will be connected with closest/farest neighbor, and "random" is random.

`corridor_curves` - style of corridors. Could be `straight` (as possible), `curved` (a lots of turnings). In case of random, this parameter sets randomly to `straight` or `curved` for each corridor

`max_connections_delta` - this parameter is needed to delete excess corridors (if it's possible, considering "are_connected" parameter)


How to use
-----------

`dungeoun.py` - algorithm module;

`printer.py` - simplest module for output;

`main.py` - entry point.

To use this module in your project you only need `dungeon.py`.

An example usage is in the `main.py`.

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
