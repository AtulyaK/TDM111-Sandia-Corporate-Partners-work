import matplotlib.pyplot as plt
import numpy as np
def line_graph(output_file_name_graph, percent,percent_placement_dict):
    """graphs the overall data into a line graph based on percentage remaining and Prediction Accuracy
    
    Arguments:
        output_file_name_graph: the path to the graphing file
        percent: a list of percentages
        percent_placement_dict: a dictionary of the top X and the number of times they showed up
        
    Returns:
        Nothing just writes a png to a file
    Students:
        Atulya Kadur
    """
    
    x = np.arange(len(percent))
    width = 0.3
    fig, ax = plt.subplots(layout='constrained')
    ax.plot(percent_placement_dict['Top 1'])
    ax.plot(percent_placement_dict['Top 3'])
    ax.plot(percent_placement_dict['Top 10'])
    ax.plot(percent_placement_dict['Top 20'])
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Correct prediction in top N')
    ax.set_title('Prediction Accuracy vs Percent of Flight Remaining')
    ax.set_xlabel('Percentage of Flight Not Truncated (Remaining)')
    ax.legend(['Top 1', 'Top 3', 'Top 10', 'Top 20'], loc = 'best', framealpha = 0)
    ax.set_xticks(x + width*1.5)
    ax.set_xticklabels([f'{i * 100:.0f}%' for i in percent], rotation=45, ha='right')
    plt.savefig(f"{output_file_name_graph}.png")