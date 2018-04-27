.DEFAULT_GOAL := run

SOURCES := source/*.py source/exchanges/*.py

.pylintrc:
	pylint --disable=locally-disabled --reports=no --generate-rcfile > $@

check: $(SOURCES) .pylintrc
	-pylint --disable=R,C $(SOURCES)

run:
	cd source/; ./RunArbiter.py

test: check
	cd source/; ./TestArbiter.py

clean:
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  *.tmp
	rm -rf __pycache__

