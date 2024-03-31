from figure_ssm import make_ssm_figure
from graph_figure1 import make_graph_figure


# TODO сделать так чтобы filename нормальный отдавался
# нужен static/Image/image-name

"""
@param Передаем путь к midi файлу, который надо обработать
@return Возвращаем путь к результату обработки (SSM)
"""
def apply_figure_ssm(filename: str) -> str:
    answer_filename, bounds = make_ssm_figure(filename)
    return answer_filename[4:]

"""
@param Передаем путь к midi файлу, который надо обработать
@return Возвращаем путь к результату обработки (картинка трек + разметка)
"""
def apply_figure(filename: str) -> str:
    answer_filename = make_graph_figure(filename)
    return answer_filename[4:]
