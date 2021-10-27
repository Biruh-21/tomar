import tinify
import environ

env = environ.Env()
environ.Env.read_env("../tomar/.env")

tinify.key(env("TINIFY_API_KEY"))
