import argparse
import json

from bokeh.plotting import figure, output_file, show
from bokeh.palettes import linear_palette, Viridis256, all_palettes
from bokeh.models import HoverTool, BoxSelectTool, ColumnDataSource


def _build_figure(dictionary, axes_labels=None, plot_width=400, plot_height=400):
    color_palette = _get_spaced_colors(len(dictionary))
    color_index = 0

    plot_figure = figure(plot_width=plot_width, plot_height=plot_height)

    if not axes_labels:
        axes_labels = {'x': 'x axis', 'y': 'y axis'}

    for lang in dictionary:
        x = []
        y = []
        for k, v in sorted(dictionary[lang].items()):
            x.append(k)
            y.append(v)

        color = color_palette[color_index]
        color_string = "rgb{}".format(color)
        # line = plot_figure.line(x, y, legend=lang, line_color=color, line_width=2, name=lang)
        line_source = ColumnDataSource({
            axes_labels['x']: x,
            axes_labels['y']: y,
            'language': [lang]*len(x),
            'color': [color_string]*len(x)
        })

        plot_figure.line(
            axes_labels['x'],
            axes_labels['y'],
            source=line_source,
            line_color=color,
            line_width=2,
            legend=lang
        )

        # _add_line_hover_tooltips(line, plot_figure, tooltips)

        color_index += 1

    tooltips = [
        ("Language", "@language"),
        (axes_labels['x'], "$x"),
        (axes_labels['y'], "$y"),
        ("Color", "<span class='bk-tooltip-color-block' "
                  "style='background-color:@color'> </span>"),
    ]

    # plot_figure.toolbar_location = None
    plot_figure.add_tools(HoverTool(tooltips=tooltips))
    return plot_figure
#
# def _add_line_hover_tooltips(line, plot_figure, tooltips):
#     plot_figure.add_tools(HoverTool(renderers=[line], tooltips=tooltips))

def plot_results(output_filename, results_dict):
    output_file(output_filename)
    axes_labels = {'x': 'err_val', 'y': 'acc'}
    plot_figure = _build_figure(results_dict, axes_labels, 800, 800)
    show(plot_figure)

def parse_result_files(input_file):
    with open(input_file) as in_file:
        results = json.load(in_file)
    return results

def _get_spaced_colors(n):
    max_value = 16581375 #255**3
    interval = int(max_value / n)
    colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]

    return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]

def _parse_arguments():
    """Parse arguments provided from command-line and return them as a dictionary."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        help="Input results file",
        action="store", dest="input_file",
        default='results.txt'
    )
    parser.add_argument(
        '-o', '--output',
        help="Output file",
        action="store", dest="output_file",
        default='graph.html'
    )

    return vars(parser.parse_args())

def main():
    arguments = _parse_arguments()
    results_dict = parse_result_files(arguments['input_file'])
    plot_results(arguments['output_file'], results_dict)


if __name__ == '__main__':
    main()
