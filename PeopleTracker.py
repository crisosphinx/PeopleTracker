from kivy.app import App
from datetime import datetime
from kivy.uix.label import Label as Lbl
from kivy.uix.button import Button as Btn
from kivy.uix.gridlayout import GridLayout as GLayout
from kivy.uix.boxlayout import BoxLayout as BLayout
from kivy.uix.tabbedpanel import TabbedPanel as TabPnl
from kivy.uix.tabbedpanel import TabbedPanelHeader as TabHdr
from kivy_garden.graph import Graph, MeshLinePlot
import json

DEBUG = False


class MainApp(App):
    def __init__(self):
        super(MainApp, self).__init__()
        self.x = .5
        self.y = .5

        self.tabs = TabPnl()
        self.tabs.default_tab_text = "Main"
        self.tabhdr = TabHdr(text='Graph')

        # Set up the amount of tallies to take in
        self.total = int()
        self.tally_mask_amt = int()
        self.tally_no_mask_amt = int()
        self.tally_take_mask_amt = int()
        self.tally_take_wo_mask_amt = int()
        self.total_txt = 'Total: '
        self.mask_txt = 'Mask: '
        self.no_mask_txt = 'No Mask: '
        self.take_mask_txt = 'Take Mask: '
        self.take_wo_mask_txt = 'Take WO Mask: '

        # Graph
        self.graph = None

        # Set up GUI
        self.total_lbl = None
        self.mask_lbl = None
        self.no_mask_lbl = None
        self.take_mask_lbl = None
        self.take_wo_mask_lbl = None
        self.tally_mask = None
        self.tally_no_mask = None
        self.tally_take_mask = None
        self.tally_take_wo_mask = None
        self.export_info = None

        # Get today's date
        _today = datetime.today()
        self.date = "{0}/{1}/{2}".format(_today.month, _today.day, _today.year)

        # Information to catalog
        self.analytics = {
            # Put in the format of tallies
            "Mask": [self.tally_mask_amt, {}],
            "NoMask": [self.tally_no_mask_amt, {}],
            "TookMask": [self.tally_take_mask_amt, {}],
            "WoMask": [self.tally_take_wo_mask_amt, {}],
            "Total": self.total
        }

    def build(self):
        _grid = GLayout(cols=1, rows=6)
        _box = BLayout(padding=10)
        _graph_box = BLayout(padding=10)
        _inside = GLayout(cols=2)
        _title = Lbl(
            text='People Tracker\n{0}'.format(self.date),
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.total_lbl = Lbl(
            text="{0}{1}".format(self.total_txt, self.total),
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.mask_lbl = Lbl(
            text="{0}{1}".format(self.mask_txt, self.tally_mask_amt),
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.no_mask_lbl = Lbl(
            text="{0}{1}".format(self.no_mask_txt, self.tally_no_mask_amt),
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.take_mask_lbl = Lbl(
            text="{0}{1}".format(self.take_mask_txt, self.tally_take_mask_amt),
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.take_wo_mask_lbl = Lbl(
            text="{0}{1}".format(self.take_wo_mask_txt, self.tally_take_wo_mask_amt),
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.tally_mask = Btn(
            text="Wearing Mask",
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.tally_no_mask = Btn(
            text="Refuse Mask",
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.tally_take_mask = Btn(
            text="No Mask, Take Mask",
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.tally_take_wo_mask = Btn(
            text="Has Mask, Take Mask",
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.export_info = Btn(
            text="Export JSON",
            size_hint=(self.x, self.y),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.graph = Logic(self.analytics)

        # Append all widgets
        _box.add_widget(_title)
        _box.add_widget(_inside)
        _inside.add_widget(self.total_lbl)
        _inside.add_widget(self.mask_lbl)
        _inside.add_widget(self.no_mask_lbl)
        _inside.add_widget(self.take_mask_lbl)
        _inside.add_widget(self.take_wo_mask_lbl)
        _grid.add_widget(widget=_box)
        _grid.add_widget(widget=self.tally_mask)
        _grid.add_widget(widget=self.tally_no_mask)
        _grid.add_widget(widget=self.tally_take_mask)
        _grid.add_widget(widget=self.tally_take_wo_mask)
        _grid.add_widget(widget=self.export_info)

        _graph_box.add_widget(widget=self.graph)

        self.tabs.add_widget(widget=self.tabhdr)
        self.tabs.default_tab_content = _grid
        self.tabhdr.content = _graph_box

        self.add_functionality()

        return self.tabs

    def add_functionality(self):
        """
        Bind events to the buttons.
        :return:
        """

        self.tally_mask.bind(on_press=lambda x: self.tallier(0))
        self.tally_no_mask.bind(on_press=lambda x: self.tallier(1))
        self.tally_take_mask.bind(on_press=lambda x: self.tallier(2))
        self.tally_take_wo_mask.bind(on_press=lambda x: self.tallier(3))
        self.export_info.bind(on_press=lambda x: self.export_doc())

        self.tabhdr.bind(on_press=lambda x: self.graph.update())

    def tallier(self, _input=int()):
        """
        Press buttons and get results.

        :param _input: Passed input.
        :return:
        """

        _get_time = str(datetime.today().time()).split(".")[0]
        if _input == 0:
            self.tally_mask_amt += 1
            self.analytics["Mask"][0] = self.tally_mask_amt
            self.analytics["Mask"][1].setdefault(self.tally_mask_amt, _get_time)
            self.mask_lbl.text = "{0}{1}".format(self.mask_txt, self.tally_mask_amt)

        if _input == 1:
            self.tally_no_mask_amt += 1
            self.analytics["NoMask"][0] = self.tally_no_mask_amt
            self.analytics["NoMask"][1].setdefault(self.tally_no_mask_amt, _get_time)
            self.no_mask_lbl.text = "{0}{1}".format(self.no_mask_txt, self.tally_no_mask_amt)

        if _input == 2:
            self.tally_take_mask_amt += 1
            self.analytics["TookMask"][0] = self.tally_take_mask_amt
            self.analytics["TookMask"][1].setdefault(self.tally_take_mask_amt, _get_time)
            self.take_mask_lbl.text = "{0}{1}".format(self.take_mask_txt, self.tally_take_mask_amt)

        if _input == 3:
            self.tally_take_wo_mask_amt += 1
            self.analytics["WoMask"][0] = self.tally_take_wo_mask_amt
            self.analytics["WoMask"][1].setdefault(self.tally_take_wo_mask_amt, _get_time)
            self.take_wo_mask_lbl.text = "{0}{1}".format(self.take_wo_mask_txt, self.tally_take_wo_mask_amt)

        self.total += 1
        self.analytics['Total'] = self.total
        self.total_lbl.text = "{0}{1}".format(self.total_txt, self.total)

    def export_doc(self):
        if DEBUG:
            print(self.analytics)

        with open("analytics_{0}.json".format(self.date).replace("/", "_"), "w") as f:
            json.dump(self.analytics, f)


class Logic(BLayout):
    def __init__(self, information=None):
        super(Logic, self).__init__()

        if information is None:
            information = dict()

        self.information = information

        self.mi = dict()
        self.nmi = dict()
        self.tmi = dict()
        self.twomi = dict()

        self.graph = Graph(
            xlabel='X', ylabel='Y', x_ticks_minor=.25, x_ticks_major=1,
            y_ticks_minor=1, y_ticks_major=1,
            y_grid_label=True, x_grid_label=True, padding=5,
            x_grid=True, y_grid=True, xmin=-1, xmax=24, ymin=-1, ymax=1
        )
        self.red_plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.gre_plot = MeshLinePlot(color=[0, 1, 0, 1])
        self.blu_plot = MeshLinePlot(color=[0, 0, 1, 1])
        self.yel_plot = MeshLinePlot(color=[1, 1, 0, 1])

        self.add_widget(widget=self.graph)

    def parse_information(self):
        if len(self.information.values()) > 0:
            self.mi = self.information['Mask'][1]
            self.nmi = self.information['NoMask'][1]
            self.tmi = self.information['TookMask'][1]
            self.twomi = self.information['WoMask'][1]

            self.graph.ymax = self.information["Total"] + 5

            self.red_plot.points = [(self.set_float(y), x) for x, y in zip(self.mi.keys(), self.mi.values())]
            self.gre_plot.points = [(self.set_float(y), x) for x, y in zip(self.nmi.keys(), self.nmi.values())]
            self.blu_plot.points = [(self.set_float(y), x) for x, y in zip(self.tmi.keys(), self.tmi.values())]
            self.yel_plot.points = [(self.set_float(y), x) for x, y in zip(self.twomi.keys(), self.twomi.values())]

    @staticmethod
    def set_float(_input=str()) -> float:
        # format is 00:00:00
        # We need 00.00

        _time = _input.split(":")
        _hour = int(_time[0]) * 1.0
        _minute = int(_time[1]) / 60.0
        _float = _hour + _minute

        return _float

    def update(self):
        self.parse_information()
        self.graph.add_plot(self.red_plot)
        self.graph.add_plot(self.gre_plot)
        self.graph.add_plot(self.blu_plot)
        self.graph.add_plot(self.yel_plot)


if __name__ == '__main__':
    app = MainApp()
    app.title = "People Tracker"
    app.run()
