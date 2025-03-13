# Systems simulation - Search neighbor particles

## Generate input files 
#### Usage
```
generate_random_input.py [-h] [--radius RADIUS] [--min_radius MIN_RADIUS] [--max_radius MAX_RADIUS] [--N Number of particles] [--L Matrix side length]
```

#### Example of usage with fixed radius
```
python generate_random_input.py --N 100 --L 5 --radius 0.2 
```

#### Example of usage with min and max radius
```
python generate_random_input.py --N 100 --L 5 --min_radius 0.1 --max_radius 0.2
```

## Cell Index Method - Search neighbor particles
#### Usage
```
usage: main.py [-h] [--static_file STATIC_FILE] [--dynamic_file DYNAMIC_FILE] [--output_file OUTPUT_FILE] [--rc RC] [--m M] --periodic_boundaries PERIODIC_BOUNDARIES --brute_force BRUTE_FORCE

Cell Index Method Simulation

options:
  -h, --help            Show this help message and exit
  
  --static_file         STATIC_FILE
                        Path to the static input file
                        
  --dynamic_file        DYNAMIC_FILE
                        Path to the dynamic input file
                        
  --output_file         OUTPUT_FILE
                        Path to the output file. Default to 'out.txt'
                        
  --rc                  RC               
                        Interaction radius for the Cell Index Method
                        
  --m                   M                 
                        Integer, Grid dimension for the Cell Index Method
                        
  --periodic_boundaries [True | False]
                        Use periodic boundaries
                        
  --brute_force         [True | False]
                        Use brute force method

````
Example of usage: 
```
python main.py --static_file particles_static.txt --dynamic_file particles_dynamic.txt --rc=1 --m=5 --brute_force False --periodic_boundaries False
```
