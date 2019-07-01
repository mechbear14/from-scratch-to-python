def get_2d(x, y, z, w, h, p):
    bx = -z / p * w / 2
    by = -z / p * h / 2
    render_x = bx + get_scaled_r(x, z, p)
    render_y = by + get_scaled_r(y, z, p)
    return render_x, render_y


def get_scaled_r(r, z, p):
    return (1 + z / p) * r


def get_circle(x, y, r):
    return x - r, y - r, x + r, y + r