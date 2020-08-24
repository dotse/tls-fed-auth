DRAFT=		tls-fed-auth

# https://github.com/miekg/mmark
MMARK=		mmark

# https://pypi.python.org/pypi/xml2rfc
XML2RFC=	venv/bin/xml2rfc

MD=		$(DRAFT).md
XML=		$(DRAFT).xml
TXT=		$(DRAFT).txt
HTML=		$(DRAFT).html


.PHONY: txt xml html clean test


txt: $(TXT)

xml: $(XML)

html: $(HTML)

%.txt: %.xml
	$(XML2RFC) $< $@

%.xml: %.md
	$(MMARK) $< > $@

%.html: %.md
	$(MMARK) -html $< > $@

clean:
	rm -f $(XML) $(TXT) $(HTML)

test:
	python3 schemacheck.py --input example.json tls-fed-metadata.yaml

venv:
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt
