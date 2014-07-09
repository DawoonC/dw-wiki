import re
import os
import jinja2
import hashlib
import random
import string
import hmac
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

SECRET = "secretmakeswomanawoman"

""" signup validation """
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)


""" password hashing """
def make_salt(length=5):
	return ''.join(random.choice(string.letters) for i in range(length))

def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	hashed = hashlib.sha256(name+pw+salt).hexdigest()
	return "%s|%s" % (hashed,salt)

def valid_pw(name, pw, hashed):
	salt = hashed.split('|')[1]
	return hashed == make_pw_hash(name, pw, salt)

def users_key(group = 'default'):
	return db.Key.from_path('users', group)


""" cookie hashing """
def make_secure_val(s):
	hashed = hmac.new(SECRET, s).hexdigest()
	return "%s|%s" % (s, hashed)

def check_secure_val(h):
	val = h.split("|")[0]
	if h == make_secure_val(val):
		return val

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)
