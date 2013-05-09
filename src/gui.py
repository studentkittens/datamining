#!/usr/bin/env python
# encoding: utf-8

# System Libraries
import os
import sys
import math
import logging

# GUI Stuff (Pango for font rendering)
from gi.repository import Gtk
from gi.repository import Pango

# Chartdrawing
from pycha.line import LineChart


def get_theme_color(widget, background=True, state=Gtk.StateFlags.SELECTED):
    color = None
    sctx = widget.get_style_context()
    if background:
        color = sctx.get_background_color(state)
    else:
        color = sctx.get_color(state)

    # convert color to a string (used by pycha)
    return '#{r:0^2x}{g:0^2x}{b:0^2x}'.format(
            r=int(255 * color.red),
            g=int(255 * color.green),
            b=int(255 * color.blue)
    )


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
        'left': 30,
        'right': 30,
        'top': 30,
        'bottom': 30
    },
    'stroke': {
        'width': 3,
        'shadow': True
    },
    'title': 'Dokumentenähnlichkeit im Cluster',
    'titleFontSize': 10
}


class TreeVis(Gtk.ApplicationWindow):
    def __init__(self, app, tree_data):
        Gtk.Window.__init__(self, title="TreeVis", application=app)
        self.set_default_size(350, 200)
        self.set_border_width(3)

        # Load UI Definition file
        builder = Gtk.Builder()
        ui_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'ui.glade'
        )
        builder.add_from_file(ui_path)

        # Data
        self.tree_data = tree_data
        self.tree_map = {}
        self.selected_cluster = None
        self.selected_doc = None

        # Widgets
        self.tree = builder.get_object('tree')
        self.list = builder.get_object('list')
        self.chartarea = builder.get_object('chartarea')
        self.docview = builder.get_object('docview')
        self.vocview = builder.get_object('vocview')

        # Models
        self.tree_store = Gtk.TreeStore(str)
        self.tree.set_model(self.tree_store)
        self.list_store = Gtk.ListStore(str)
        self.list.set_model(self.list_store)
        self.docbuffer = self.docview.get_buffer()
        self.voc_store = Gtk.ListStore(str, int, str)
        self.vocview.set_model(self.voc_store)

        # Styling for the Textview
        self.bold_tag = self.docbuffer.create_tag(
                'head', size_points=16,
                weight=Pango.Weight.BOLD,
                underline=Pango.Underline.DOUBLE
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
        self.vocview.append_column(
                Gtk.TreeViewColumn('Vocabulary', Gtk.CellRendererText(), text=0)
        )
        self.vocview.append_column(
                Gtk.TreeViewColumn(
                    'Normalized Frequency',
                    Gtk.CellRendererProgress(),
                    value=1, text=2
                )
        )

        # Configure chart colors (take them from the theme)
        self._configure_chart_colors()

        # Add root widget to Window
        self.add(builder.get_object('top_paned'))

        # Fill in data
        self._fill_tree()
        self._fill_list('')

        # ChartArea should be redrawn on resize
        self.chartarea.connect('draw', self.on_chart_draw)

        # Selection
        for model, func in [(self.tree, self.on_tree_select), (self.list, self.on_list_select)]:
            model_selection = model.get_selection()
            model_selection.connect('changed', func)
            model_selection.select_path('0')

        # Draw something in the text window
        self.on_list_select(self.list.get_selection())

    def _configure_chart_colors(self):
        # Make chart color look like the highlighted theme color
        CHART_OPTIONS['colorScheme']['args']['initialColor'] = get_theme_color(
                self.tree, True, Gtk.StateFlags.SELECTED
        )

    def _fill_tree(self):
        # Clear previous data
        self.tree_map = {}
        self.tree_store.clear()

        tree_iter = None
        nodes = [(self.tree_data, tree_iter)]

        while len(nodes) is not 0:
            childs = []
            for node, tree_iter in nodes:
                curr_iter = self.tree_store.append(tree_iter, (node.name,))
                self.tree_map[node.name] = node
                if node.left is not None:
                    childs.append((node.left, curr_iter))
                if node.right is not None:
                    childs.append((node.right, curr_iter))

            nodes = childs

        self.tree.expand_all()

    def _fill_list(self, selected_cluster):
        # Clear previous data
        self.list_store.clear()

        cluster = self.tree_map.get(selected_cluster, None)
        if cluster is not None:
            self.selected_cluster = cluster
            for doc in cluster.docs:
                self.list_store.append((doc.path,))

    def _fill_docview(self, heading, body):
        self.docbuffer.set_text('')

        for style, text in [(self.bold_tag, heading), (self.norm_tag, body)]:
            pos = self.docbuffer.get_end_iter()
            self.docbuffer.insert_with_tags(pos, text + '\n\n', style)

    def _fill_voc_list(self, doc):
        self.voc_store.clear()

        result = []
        for idx, voc in enumerate(doc.vocs):
            result.append((
                voc, doc.norm_freq[idx] * 100,
                str(int(doc.abs_freq[idx]))
            ))

        for item in set(result):
            self.voc_store.append(item)

    def on_list_select(self, selection):
        '''Called when user selects a document in the List

        Updates the content of the TextView and re-renders chart.
        '''
        # This should not happen, except on startup
        if self.selected_cluster is None:
            return

        model, tree_iter = selection.get_selected()
        if tree_iter is not None:
            doc_name = model[tree_iter][0]
            for doc in self.selected_cluster.docs:
                if doc.path == doc_name:
                    self.selected_doc = doc
                    self._fill_docview(doc.path, doc.text)
                    self._fill_voc_list(doc)
                    break
            else:
                logging.debug('Warning: No documents to display.')

        # Update chart
        self.chartarea.queue_draw()

    def on_tree_select(self, selection):
        # Refill documents list
        model, tree_iter = selection.get_selected()
        if tree_iter is not None:
            self._fill_list(model[tree_iter][0])

        # Auto-select first item
        self.list.get_selection().select_path('0')

        # Redraw chart
        self.chartarea.queue_draw()

    def on_chart_draw(self, widget, ctx):
        # This should not happen actually, but be sure.
        if self.selected_cluster and self.selected_doc:
            lines = []
            for doc in self.selected_cluster.docs:
                distance = self.selected_doc.distances[doc.name]
                cut_path = os.path.basename(doc.path)
                lines.append((cut_path[-5:-1], math.log10(distance * 100 + 1) / 2.0))

            if len(lines) > 1:
                # This matches the chart background color
                ctx.set_source_rgb(0.96, 0.96, 0.96)
                ctx.paint()

                # Build actual indexed dataset from lines
                dataSet = (
                    ('docs', [(i, l[1]) for i, l in enumerate(lines)]),
                )

                # Grid legend scaling
                CHART_OPTIONS['axis']['x']['ticks'] = [dict(v=i, label=l[0]) for i, l in enumerate(lines)]

                # Actually draw the chart on the surface provided by ctx
                chart = LineChart(ctx.get_target(), CHART_OPTIONS)
                chart.addDataset(dataSet)
                chart.render()
            else:
                # No data to display, so just display a nicely rendererd "NO!
                alloc = widget.get_allocation()
                ctx.set_source_rgb(0.5, 0.5, 0.5)

                # Draw text exactly centered in the widget center, with a
                # certain offset in height
                def draw_center_text(text, font_size=15, height_off=0):
                    ctx.set_font_size(font_size)
                    extents = ctx.text_extents(text)
                    ctx.move_to(alloc.width / 2 - extents[2] / 2, alloc.height / 2 - height_off)
                    ctx.show_text(text)

                # Now you gonna see if your font is good :-)
                draw_center_text('№', 100, +30)
                draw_center_text('⦃ only one document in cluster ⦄')

                # Draw current state
                ctx.stroke()


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
    return app.run([])


if __name__ == '__main__':
    from maketree import maketree
    show_treevis(maketree())
