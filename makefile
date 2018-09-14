.DEFAULT_GOAL := install

SOURCES := source/*.py source/exchanges/*.py

check: $(SOURCES) .pylintrc
	-pylint --disable=R,C $(SOURCES)

install:
	( \
       source venv/bin/activate; \
       sudo pip install -r requirements.txt; \
    )

run:
	cd source/; ./RunArbiter.py

test: check
	cd source/; ./TestArbiter.py

clean:
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  *.tmp
	rm -rf __pycache__

