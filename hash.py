import hashlib

s = None

a = s.encode('utf-8')
print(hashlib.md5(a).hexdigest())
print(hashlib.sha1().hexdigest())