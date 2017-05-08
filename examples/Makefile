PRIVATE_KEYS=	private.json
PUBLIC_KEYS=	public.json

UNSIGNED_DATA=	../example.json
SIGNED_DATA=	signed.json

sign:
	python3 ../tools/sign.py --signer $(PRIVATE_KEYS) \
		--input $(UNSIGNED_DATA)  --output $(SIGNED_DATA)

verify:
	python3 ../tools/verify.py --trusted $(PUBLIC_KEYS) --input $(SIGNED_DATA)

clean:
	rm -f $(SIGNED_DATA)
