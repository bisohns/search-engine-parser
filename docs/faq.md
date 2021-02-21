# FAQ

## Why do I get `RuntimeError: This event loop is already running` When running in Jupyter Notebook

This is a popular issue on [Jupyter Notebook](https://github.com/jupyter/notebook/issues/5663). The solution:
- try `pip install --upgrade ipykernel ipython` which should upgrade the ipykernet to a recent version with issue resolved
- or add this to your notebook to allow nested asyncio loops
```bash
!pip install nest-asyncio
```

```python
import nest_asyncio
nest_asyncio.apply()
```

