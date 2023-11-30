from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainterPath, QPen, QColor
from PyQt6.QtWidgets import (QTreeWidgetItem, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem,
                             QGraphicsPathItem, QGraphicsItemGroup)
from PyQt6 import QtGui
from typing import List, Union, Optional, Tuple, Dict, Any, TypedDict
import numpy as np
import os
import pydicom as pyd
from icecream import ic
from npo.beato import constant as BC

KEY_WW = (0x0028, 0x1051)
KEY_WL = (0x0028, 0x1050)


def get_point_on_view(sp: QPointF, color: str, r: Union[int, float]):
    cx, cy = sp.x(), sp.y()
    qp = QGraphicsEllipseItem(cx, cy, r, r)
    qp.setStartAngle(0)
    qp.setSpanAngle(360)
    qp.setBrush(QColor(color))
    qp.setPen(QPen(QColor(color)))
    return qp



def get_graphics_item(prompt_type: BC.PromptType):
    if prompt_type == BC.PromptType.BOX:
        return QGraphicsRectItem()
    elif prompt_type == BC.PromptType.CLICK:
        return QGraphicsEllipseItem()
    elif prompt_type == BC.PromptType.MASK:
        return QGraphicsPolygonItem()
    elif prompt_type == BC.PromptType.DOODLE:
        return QGraphicsItemGroup()


# def get_lt_rb(p1: QPointF, p2: QPointF):
#     QPointF.


def get_device_list():
    results = ['cpu']
    return results


def get_default_ww_wl(dfile: pyd.FileDataset):
    ww, wl = dfile.setdefault(KEY_WW, None).value, dfile.setdefault(KEY_WL, None).value
    if ww is None or wl is None:
        maxi = ic(dfile.pixel_array.max())
        mini = ic(dfile.pixel_array.min())
        ww = int(abs(maxi - mini))
        wl = int(maxi + mini) // 2

    return [ww, wl]


def extract_info_from_event(event, dfile: pyd.FileDataset, frame_idx, pos):
    """
        extract the (x, y) maybe has wheel angle that divided by -120 degree.
    :param dfile:
    :param event:
    :param frame_idx:
    :param width:
    :param height:
    :return: all key: 'x', 'y', 'wheel'
    """
    # try:
    results = {}
    dicom_w, dicom_h = dfile.Columns, dfile.Rows
    # x_bias = (width - dicom_w) // 2
    # y_bias = (height - dicom_h) // 2
    #
    x, y = int(pos.x()), int(pos.y())
    results['x'] = x
    results['y'] = y

    if 0 <= x < dicom_w and 0 <= y < dicom_h:
        results['value'] = dfile.pixel_array[int(frame_idx), x, y]
    else:
        results['value'] = None

    if isinstance(event, QtGui.QWheelEvent):
        return results, frame_idx + event.angleDelta().y() // -120

    return results
    # except Exception as e:
    #     print(e)


def read_dicom(path_obj: Union[QTreeWidgetItem, str]) -> pyd.FileDataset:
    if not isinstance(path_obj, str):
        print('GG')
        path_obj = f'{path_obj.parent().text(0)}/{path_obj.text(0)}'

    dfile = pyd.read_file(path_obj)
    return dfile


def debug(func):
    def wrapper():
        try:
            return func()
        except Exception as e:
            print(e)
            return e
    return wrapper()


def dicom_map2_rgb(dimg: np.ndarray, ww: int, wl: int) -> np.ndarray:
    dimg = dimg.astype(np.float32)
    interval = [wl - ww / 2, wl + ww / 2]
    dimg[dimg < interval[0]] = interval[0]
    dimg[dimg > interval[1]] = interval[1]
    dimg = (dimg - interval[0]) / (interval[1] - interval[0])
    dimg *= 255
    return dimg.astype(np.uint8)


def handle_path_input(path_list: List[str]) -> List[str]:
    first_path = path_list[0]

    if os.path.isdir(first_path) and len(path_list) == 1:
        path_list = [f'{first_path}/{name}' for name in os.listdir(first_path)]

    return path_list


def coordinate_convertor(in_point, image_size, scene_size):
    if isinstance(in_point, QtGui.QEventPoint):
        # x, y = in_point.
        pass

def find_target_widget(target_name):
    pass


class LimitNumber(object):
    def __init__(self, value, limit):
        super().__init__()
        self.limit = limit
        self.value = value

    def __add__(self, other):
        if isinstance(other, LimitNumber):
            assert other.limit == self.limit, f"Limit {self.limit}, {other.limit} doesn't match"
            value = self.value + other.value
        elif isinstance(other, int):
            value = self.value + other

        value %= self.limit

        return LimitNumber(value, self.limit)

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.value + 1}/{self.limit}'
