from sdl2 import SDL_Surface

def load_img(path: str, as_argb: bool = True)-> SDL_Surface: ...
def load_image(fname: str, enforce: str | None = None)-> SDL_Surface: ...
