
Setup vitualenv with Python3. This only needs to be done once.
```
cd dp-viz-gen
sudo pip install virtualenv      # This may already be installed
virtualenv -p python3.4 .env   	 # Create a virtual environment (python3)
source .env/bin/activate         # Activate the virtual environment
pip install -r requirement.txt   # Install dependencies

# After you are done
deactivate                       # Exit the virtual environment
```


Start example notebook 
```
source .env/bin/activate         # Activate the virtual environment

# setting up dpcomp paths

export DPCOMP_CORE=$HOME/Github/dpcomp_core_op  
export PYTHONPATH=$PYTHONPATH:$DPCOMP_CORE/
export PYTHONPATH=$PYTHONPATH:$DPCOMP_CORE/tests

jupyter notebook

# After you are done
deactivate                       # Exit the virtual environment
```

There are two interfaces provided by the module `MyHeatmap`: `drawHeatMap` and `drawHeatMapSmooth`.


General Parameters:
- `name`: name of input histogram, needs a .npy file.
- `transformFunc`: the function describing preprocessing of the input histogram. The commonly used one is logNorm function which maps value to the range of [-1,1]. 
- `cmap`: colormap used for heatmap, can be continuous or discrete.
- `nonNegative`: if True, then all negative values will be rounded up to 0.
- `outName`: if specified, save file with the name.
- `dpi`: set to the width of histogram (need to be square) if saving the figure to the same dimension as the histogram. e.g, set dpi=256 will generate a 256pi*256pi figure for a 256*256 histogram.

Smoothing related:
- `uniformBin`: if True, use uniform bin size for the binning of **colormap**.

- `deltaD`: if non-uniform binning is used, deltaD is the indistinguishable threshold for the smoothing technique. For independent laplace noise with espilon = 0.1, the value is around 53. 

    Note: The dpi setting only controls the dimension of saved figure. The one shown in the notebook is just a preview, please use the image save to local directory if the dimension is important.


