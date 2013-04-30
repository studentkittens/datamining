import os
import sys

from gi.repository import Gtk
from gi.repository import Pango

from pycha.line import LineChart


CHART_OPTIONS = {
    'axis': {
        'x': {
            'ticks': []
        },
        'y': {
            'tickCount': 4,
        }
    },
    'background': {
        'color': '#eeeeff',
        'lineColor': '#444444'
    },
    'colorScheme': {
        'name': 'gradient',
        'args': {
            'initialColor': 'blue',
        },
    },
    'legend': {
        'hide': True,
    },
    'padding': {
        'left': 5,
        'right': 5,
        'top': 5,
        'bottom': 5
    },
    'stroke': {
        'width': 3,
        'shadow': True
    },
    'title': 'Dokumentenähnlichkeit im Cluster',
    'titleFontSize': 10
}


LOREM = ''' Eget. Dolor est cursus primis fames semper vestibulum. Nibh arcu, neque fusce, nam habitasse. Pulvinar. Elit fusce sodales mollis ve cras pede. Tellus odio dis viverra dis, mi ipsum. Arcu pulvinar class ad urna turpis rhoncus in, nunc. Magnis fusce arcu aenean porttitor mi, donec pellentesque accumsan velit sollicitudin, penatibus dictum ut diam. Ante litora hendrerit. Quam quis leo. Quam magna eu orci. Ante a elit risus. Viverra, nisl pulvinar ut, nisl inceptos. Pede sociis augue dictum malesuada. Placerat tempor quam erat mollis, litora ad. Montes ipsum blandit rutrum dolor primis fames enim scelerisque at, nostra ad augue. Etiam iaculis id, iaculis id, velit pharetra. Ve ornare. Dignissim massa ut fames ac mi erat odio fusce eros eu consectetuer commodo.
Tincidunt id, imperdiet adipiscing, conubia orci in sollicitudin aptent, congue, fames. Malesuada justo eu fermentum posuere, tempus ridiculus ad, in odio. Sociis odio ad. Augue eget netus, eu nam duis class lacus, sapien hendrerit volutpat, id ligula. Hendrerit faucibus montes aptent hendrerit ve, turpis. Nibh torquent eu, ullamcorper ad, aptent. Enim orci duis. Nisi vivamus sodales nonummy ornare nulla parturient ve, lobortis. Porta magnis sagittis malesuada ac, nullam conubia semper nibh dictum. Ad, venenatis nulla, venenatis volutpat quis nullam facilisi neque eni pede, leo. Elit tortor adipiscing vitae urna, ac sollicitudin turpis risus. Duis ipsum hymenaeos. Vehicula ad condimentum orci, curabitur dui, blandit et, eu lorem vulputate maecenas ad condimentum pede. Ve condimentum pede, nisl, pharetra a, maecenas. At amet, ornare tristique mi, in mattis consectetuer dapibus.
Morbi vulputate. Libero. Purus volutpat parturient imperdiet. Elit erat, dui dolor varius euismod mauris. Sit pede sed nulla purus, dis. Mus nulla neque, sociosqu massa dui netus porttitor vehicula. Imperdiet netus sit donec nam lobortis consequat at amet metus ornare quam. Consectetuer potenti vitae eu habitasse nulla. Posuere interdum. Cras, rhoncus odio, ad donec ad consequat condimentum, class consequat neque ante. Molestie, penatibus porta ultricies habitant. Tempus ac sit convallis purus nisi vitae rhoncus nonummy. Cras lorem facilisis lobortis porta venenatis cubilia nunc. Lacus tempus fusce donec. Cursus varius massa id non porttitor aenean dui lectus proin vestibulum. Curae, duis urna.
Mattis. Sapien, non ante pharetra conubia nascetur mi. Dis nibh elit hymenaeos mauris nascetur neque nulla aliquet sagittis enim mauris non. Pretium tempor etiam sociis litora massa per diam parturient semper in eros turpis leo mollis laoreet. Dolor justo nec parturient venenatis, diam rhoncus curae magna fermentum. Habitasse, lorem imperdiet nulla venenatis ac. Habitant, erat rhoncus eget, et quam. Massa cursus ac accumsan nec, risus. Placerat ad sit montes ut. Arcu. Metus scelerisque vehicula aliquam erat urna dui. At, vitae pharetra per. At. Sociis a, praesent quam tellus ac ligula mi, praesent amet imperdiet eleifend. Quis. Facilisi nisi cras ultricies pellentesque. Magnis maecenas consequat fusce nisl dictum, ve cras ipsum praesent, penatibus.
'''


class TreeVis(Gtk.ApplicationWindow):
    def __init__(self, app, tree_data):
        Gtk.Window.__init__(self, title="TreeVis", application=app)
        self.set_default_size(350, 200)
        self.set_border_width(3)

        builder = Gtk.Builder()
        ui_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'ui.glade'
        )
        builder.add_from_file(ui_path)

        # Widgets
        self.data = tree_data
        self.tree = builder.get_object('tree')
        self.list = builder.get_object('list')
        self.chartarea = builder.get_object('chartarea')
        self.docview = builder.get_object('docview')

        # Models
        self.tree_store = Gtk.TreeStore(str)
        self.tree.set_model(self.tree_store)
        self.list_store = Gtk.ListStore(str)
        self.list.set_model(self.list_store)
        self.docbuffer = self.docview.get_buffer()

        # Styling (Make header bold)
        self.bold_tag = self.docbuffer.create_tag(
                'head', size_points=16, weight=Pango.Weight.BOLD
        )

        self.norm_tag = self.docbuffer.create_tag(
                'norm', size_points=10
        )

        # Columns
        self.tree.append_column(Gtk.TreeViewColumn(
            'Treeview', Gtk.CellRendererText(), text=0)
        )
        self.list.append_column(
                Gtk.TreeViewColumn('Documents', Gtk.CellRendererText(), text=0)
        )

        # Add root widget to Window
        self.add(builder.get_object('grid'))

        # Fill in data
        self._fill_tree()
        self._fill_list()

        # ChartArea should be redrawn on resize
        self.chartarea.connect('draw', self.on_chart_draw)

        # Selection
        for model, func in [(self.tree, self.on_tree_select), (self.list, self.on_list_select)]:
            model_selection = model.get_selection()
            model_selection.connect('changed', func)
            model_selection.select_path('0')

    def _fill_tree(self):
        tree_iter = None
        for item in 'ABCDE':
            tree_iter = self.tree_store.append(tree_iter, (item,))

        self.tree.expand_all()

    def _fill_list(self):
        for i in range(10):
            self.list_store.append(('Document ' + str(i),))

    def _fill_docview(self, heading, body):
        self.docbuffer.set_text('')

        for style, text in [(self.bold_tag, heading), (self.norm_tag, body)]:
            pos = self.docbuffer.get_end_iter()
            self.docbuffer.insert_with_tags(pos, text + '\n\n', style)

    def on_list_select(self, selection):
        '''Called when user selects a document in the List

        Updates the content of the TextView and re-renders chart.
        '''
        model, tree_iter = selection.get_selected()
        if tree_iter is not None:
            self._fill_docview(model[tree_iter][0], LOREM)

    def on_tree_select(self, selection):
        model, tree_iter = selection.get_selected()
        if tree_iter is not None:
            self._fill_docview(model[tree_iter][0], LOREM)

    def on_chart_draw(self, widget, ctx):
        lines = (
            ('bar.py', 319),
            ('chart.py', 875),
            ('color.py', 204),
            ('line.py', 130),
            ('pie.py', 352),
            ('scatter.py', 38),
            ('stackedbar.py', 121),
            ('radar.py', 323),
        )

        dataSet = (
            ('lines', [(i, l[1]) for i, l in enumerate(lines)]),
        )

        CHART_OPTIONS['axis']['x']['ticks'] = [dict(v=i, label=l[0]) for i, l in enumerate(lines)]

        chart = LineChart(ctx.get_target(), CHART_OPTIONS)
        chart.addDataset(dataSet)
        chart.render()


class TreeVisApplication(Gtk.Application):
    def __init__(self, tree_data):
        Gtk.Application.__init__(self)
        self.tree_data = tree_data

    def do_activate(self):
        win = TreeVis(self, self.tree_data)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


def show_treevis(tree):
    app = TreeVisApplication(tree)
    return app.run(sys.argv)


show_treevis(None)
