rm -rf .eggs/
rm -rf fastapi_router_controller.egg-info/
rm -rf dist/

git pull

python setup.py sdist
twine upload dist/*