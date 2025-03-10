# Systems simulation - Search neighbor particles

## Generate input files 
#### Usage
```
generate_random_input.py [-h] [--radius RADIUS] [--min_radius MIN_RADIUS] [--max_radius MAX_RADIUS] N L
```

#### Example of usage with fixed radius
```
python generate_random_input.py 100 5 --radiun 0.2 
```

#### Example of usage with min and max radius
```
python generate_random_input.py 100 5 --min_radius 0.1 --max_radius 0.2
```