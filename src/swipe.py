import sys

from gi.repository import GLib, Gdk, Gtk, GtkClutter, Clutter


def _render_pixbuf(widget, width, height):
    # Use an OffscreenWindow to render the widget
    off_win = Gtk.OffscreenWindow()
    off_win.add(widget)
    off_win.set_size_request(width, height)
    off_win.show_all()

    # this is needed, otherwise the screenshot is black
    while Gtk.events_pending():
        Gtk.main_iteration()

    # Render the widget to a GdkPixbuf
    widget_pix = off_win.get_pixbuf()

    # Remove the widget again (so we can reparent it later)
    off_win.remove(widget)

    return widget_pix


def _create_texture(pixbuf, width, height, x_off=0, y_off=0):
    # Create a Clutter Texture from it
    ctex = GtkClutter.Texture()
    if pixbuf is not None:
        ctex.set_from_pixbuf(pixbuf)

    # Set some dimensions
    if x_off is not 0:
        ctex.set_x(x_off)

    if y_off is not 0:
        ctex.set_y(y_off)

    ctex.set_width(width)
    ctex.set_height(height)

    return ctex


def swipe(parent, old_widget, new_widget, right=True, time_ms=400):
    # Allocation of the old widget.
    # This is also used to determine the size of the new_widget
    alloc = old_widget.get_allocation()
    width, height = alloc.width, alloc.height

    # Get the Imagedate of the old widget
    old_pixbuf = Gdk.pixbuf_get_from_window(
            old_widget.get_window(), 0, 0, width, height
    )

    # Render the new image (which is not displayed yet)
    new_pixbuf = _render_pixbuf(
            new_widget, width, height
    )

    # Toplevel container inside the stage
    container = Clutter.Actor()

    # Left-Side Image
    container.add_child(_create_texture(
        old_pixbuf, width, height, x_off=0)
    )

    # Right-Side Image
    container.add_child(_create_texture(
        new_pixbuf, width, height, x_off=-width if not right else +width)
    )

    # Shuffle widgets around
    embed = GtkClutter.Embed()
    embed.get_stage().add_child(container)
    parent.remove(old_widget)
    parent.add(embed)
    parent.show_all()

    # Actual animation:
    transition = Clutter.PropertyTransition()
    transition.set_property_name('x')
    transition.set_duration(time_ms)
    transition.set_from(0)

    if right:
        transition.set_to(-width)
    else:
        transition.set_to(+width)

    # Now go back to normal and swap clutter with the new widget
    def restore_widget(*args):
        parent.remove(embed)
        parent.add(new_widget)
        parent.show_all()

    # Be notified when animation ends
    transition.connect('completed', restore_widget)

    # Play the animation
    container.add_transition('animate-x', transition)


# Initialization that has to been done always
GtkClutter.init(sys.argv)

if __name__ == '__main__':
    class SwipeWin(Gtk.ApplicationWindow):
        def __init__(self, app):
            Gtk.ApplicationWindow.__init__(self, title='Swipe', application=app)

            self.l_butt = Gtk.Button('Go Right ⇒')
            self.r_butt = Gtk.Button('⇐ Go Left')

            self.l_butt.connect('clicked', self.on_left_button_clicked)
            self.r_butt.connect('clicked', self.on_right_button_clicked)

            # Refcounting trick
            self.add(self.l_butt)

        def on_left_button_clicked(self, button):
            swipe(self, self.l_butt, self.r_butt, right=True, time_ms=200)
            return True

        def on_right_button_clicked(self, button):
            swipe(self, self.r_butt, self.l_butt, right=False, time_ms=1000)
            return True

    class SwipeApp(Gtk.Application):
        def __init__(self):
            Gtk.Application.__init__(self)

        def do_activate(self):
            win = SwipeWin(self)
            win.show_all()

        def do_startup(self):
            Gtk.Application.do_startup(self)

    app = SwipeApp()
    app.run(sys.argv)
