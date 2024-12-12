from hashlib import sha256


asdf = "asdf".encode("UTF-8")

print(sha256(asdf).hexdigest())
