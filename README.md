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
````
