DRAFT=		scim-fed-auth

# https://github.com/miekg/mmark
MMARK=		mmark

# https://pypi.python.org/pypi/xml2rfc
XML2RFC=	xml2rfc

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
	$(MMARK) -xml2 -page $< > $@

%.html: %.md
	$(MMARK) -page $< > $@

clean:
	rm -f $(XML) $(TXT) $(HTML)

test:
	python3 schemacheck.py --input example.json scim-fed-metadata.yaml
