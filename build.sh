cd dist/
rm *
cd ..
python setup.py sdist bdist_wheel
twine upload dist/*