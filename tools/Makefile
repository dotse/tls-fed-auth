KEYS=		../keys.json
UNSIGNED_DATA=	../example.json
SIGNED_DATA=	signed.json

sign:
	python3 sign.py --signer $(KEYS) --input $(UNSIGNED_DATA)  --output $(SIGNED_DATA)

verify:
	python3 verify.py --trusted $(KEYS) --input $(SIGNED_DATA)

clean:
	rm -f $(SIGNED_DATA)
