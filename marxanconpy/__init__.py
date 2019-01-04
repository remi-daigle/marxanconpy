import marxanconpy.marcon
import marxanconpy.metrics
import marxanconpy.manipulation
import marxanconpy.posthoc
import marxanconpy.spatial

import wx
import pandas

name = "marxanconpy"
__version__ = 'v0.1.2rc1'

def progress_bar_update(count, dlg, keepGoing, n, progressbar=True):
    """ Progress Bar Update

    Function that manages the updates for progress bar dialogs

    :param count: The total number of steps for the progress bar
    :param dlg: The progressbar dialog (wx.ProgressDialog).
    :param keepGoing:
    :param n: The number of steps to move forward
    :param progressbar: Logical. True if you want to see a progressbar
    :return:
    """
    if progressbar:
        count += n
        (keepGoing, skip) = dlg.Update(count)

def warn_dialog(message, caption="Warning!"):
    """ Warning Dialog

    Creates a warning pop-up (a wx.MessageBox)

    :param message: A string containing the contents of the warning
    :param caption: The heading caption
    :return:
    """
    wx.MessageBox(message, caption, style=wx.OK | wx.ICON_WARNING)

def read_csv_tsv(filepath):
    """ Marxan file reader

    Reads comma or tab separated Marxan input or output files. Reads as csv first, if there is only 1 column (i.e. wrong
    delimiters), then the file is read as a tsv.

    :param filepath: Filepath for file in question
    :return:
    """
    file = pandas.read_csv(filepath)
    if file.shape[1] < 2:
        file = pandas.read_csv(filepath, delimiter='\t')
    return file