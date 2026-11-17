from Settings.Settings import settings

def get_shade(depth):
    return max(0, 1 - depth / settings.view.Distance) ** 1.5