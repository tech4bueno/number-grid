# Number grid

A number grid that can be easily annotated for teaching and learning place value.

## Try

Go to https://number-grid.onrender.com (be patient: first load takes 1min+ on Render's free plan)

Open in another tab (or on a different device) to see how the annotations sync in realtime.

This way a parent can observe or annotate from a different device and not need to peer over a child's shoulder.

## Run

### With [uv](https://docs.astral.sh/uv/)

`uvx --from number-grid number-grid`

### With pip

`pip install number-grid` and then `number-grid`

### With Docker

`docker build -t number-grid .` then `docker run -p 8000:8000 number-grid`

## Develop

```
git clone https://github.com/tech4bueno/number-grid
pip install -e .[test]
pytest
```

## Deploy

Deploys easily to Render's free plan.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
