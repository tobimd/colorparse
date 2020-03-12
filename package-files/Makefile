build: 	
	@colorparse -p 1 "building with ;c/setup.py" -S -i "make-color"
	@python3 setup.py sdist bdist_wheel

publish:
	@colorparse -p 1 "using ;c/twine;: to upload package" -S -i "make-color"
	@python3 -m twine upload dist/*

test-publish:
	@colorparse -p 1 "using ;c/twine;: to upload ;RTEST;: package" -S -i "make-color"
	@python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	@colorparse -p 1 "cleaning ;c/build//;:/, ;c/dist//;:/, \
	;c/__pycache__//;:/ and ;c/*.egg-info" -S -i "make-color"
	@rm -rf build/ dist/ *.egg-info __pycache__/

copy:
	@colorparse -p 1 "symlinking ;c/colorparse.py;: here" -S -i "make-color"
	@rm -f colorparse.py
	@ln ~/.local/lib/python3.7/site-packages/colorparse.py colorparse.py
