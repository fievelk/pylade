import argparse
import json

from bokeh.plotting import figure, output_file, show
from bokeh.palettes import linear_palette, Viridis256, all_palettes
from bokeh.models import HoverTool, BoxSelectTool, ColumnDataSource


def _build_figure(dictionary, axis_labels=None, plot_width=400, plot_height=400):
    """
    `dictionary` has this structure:
        {
        'lang1':
            {
                'err_value1_1', 'accuracy1_1',
                'err_value1_2', 'accuracy1_2'
            },
        'lang2':
            {
                'err_value2_1', 'accuracy2_1',
                'err_value2_2', 'accuracy2_2'
            }
        }

    """

    if not axis_labels:
        axis_labels = {'x': 'x axis', 'y': 'y axis'}

    color_palette = _get_spaced_colors(len(dictionary))
    color_index = 0

    plot_figure = figure(
        plot_width=plot_width,
        plot_height=plot_height,
        x_axis_label = axis_labels['x'],
        y_axis_label = axis_labels['y']
   )

    for lang in dictionary:
        x_points = []
        y_points = []
        for k, v in sorted(dictionary[lang].items()):
            x_points.append(k)
            y_points.append(v)

        color = color_palette[color_index]
        color_string = "rgb{}".format(color)

        number_of_points = len(x_points)
        line_source = ColumnDataSource({
            axis_labels['x']: x_points,
            axis_labels['y']: y_points,
            'language': [lang] * number_of_points,
            'color': [color_string] * number_of_points
        })

        plot_figure.line(
            axis_labels['x'],
            axis_labels['y'],
            source=line_source,
            line_color=color,
            line_width=2,
            legend=lang
        )

        color_index += 1

    tooltips = [
        ("Language", "@language"),
        (axis_labels['x'], "$x"),
        (axis_labels['y'], "$y"),
        ("Color", "<span class='bk-tooltip-color-block' "
                  "style='background-color:@color'> </span>"),
    ]

    plot_figure.add_tools(HoverTool(tooltips=tooltips))
    return plot_figure

def plot_results(output_filename, results_dict):
    output_file(output_filename)
    axis_labels = {'x': 'err_val', 'y': 'acc'}
    plot_figure = _build_figure(results_dict, axis_labels, 800, 800)
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
