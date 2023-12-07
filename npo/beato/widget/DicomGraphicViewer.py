import typing

import torch
# import PyQt6.QtCore.QEvent
from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsRectItem, \
    QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsPixmapItem, QGraphicsItemGroup, QGraphicsPathItem
from PyQt6.QtGui import QImage, QPixmap, QEventPoint, QMouseEvent, QPen, QColor, QBrush, QPainterPath
from PyQt6.QtCore import QRect, QPoint, Qt, QPointF, QRectF
# from PyQt6.
from npo.beato import utils as BU
from npo.beato import constant as BC
from npo.beato.data import Prompt
from pydicom import (FileDataset)

from icecream import ic


class DeclaratorDicomGraphicViewer(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewer_panel = QGraphicsScene(self)
        self.viewer_panel.setObjectName('viewer_panel')

        self.setScene(self.viewer_panel)
        self.setInteractive(True)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate)
        self.setMouseTracking(True)


class DicomGraphicViewer(DeclaratorDicomGraphicViewer):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.image_item = QGraphicsPixmapItem()
        self.image_item.setPos(0, 0)
        self.mask_item = QGraphicsPixmapItem()
        self.mask_item.setPos(0, 0)
        self.viewer_panel.addItem(self.image_item)
        self.viewer_panel.addItem(self.mask_item)
        self.sw0 = None
        self.sh0 = None
        self.xb = None
        self.yb = None
        self.record_flag = False
        self.prompt_item = None
        self.start_p = None
        self.root.model_worker.MaskEvent.connect(self.show_mask)

    # def resizeEvent(self, event: typing.Optional[QtGui.QResizeEvent]) -> None:
    #     super().resizeEvent(event)
    #     dw, dh = event.oldSize().width() - event.size().width(), event.oldSize().height() - event.size().height()
    #     swo = self.viewer_panel.width()
    #     sho = self.viewer_panel.height()
    #     self.viewer_panel.setSceneRect(0, 0, swo + dw, sho + dh)
        # self.set_bias()

    # Local Event
    def wheelEvent(self, event: typing.Optional[QtGui.QWheelEvent]) -> None:
        if self.root.dicom_image is None or self.record_flag:
            return

        #  TODO: Clear the try ... except ...
        try:
            df, fi, sp = self.root.dicom_file, self.root.frame_idx, self.mapToScene(event.position().toPoint())
            results, new_idx = BU.extract_info_from_event(event, df, fi, sp)

            self.root.update_frame_idx(new_idx)
            self.plot_dicom(*self.root.ww_wl)
            self.root.show_cursor_info(**results)

        except Exception as e:
            print(f'WheelEvent: {e}')

    #  TODO: Clear the try ... except ...
    # Local Event
    def mouseMoveEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        if self.root.dicom_image is None:
            return
        self.show_information_on_status_bar(event)

        if not self.record_flag:
            return

        cp = self.mapToScene(event.pos())
        # Handle Prompt visualization.
        if self.root.prompt_mode == BC.PromptType.CLICK:
            pass
        elif self.root.prompt_mode == BC.PromptType.BOX:
            try:
                self.build_bbox_prompt(cp)
            except Exception as e:
                print(e)
        elif self.root.prompt_mode == BC.PromptType.DOODLE:
            try:
                self.build_doodle_prompt(cp)
            except Exception as e:
                print(e)
            pass
        elif self.root.prompt_mode == BC.PromptType.MASK:
            pass

    #  TODO: Clear the try ... except ...
    def mousePressEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        pm = self.root.prompt_mode

        if event.button() != Qt.MouseButton.LeftButton or pm == BC.PromptType.DEFAULT or self.root.dicom_image is None:
            return
        print(f'Pressed!')
        if self.prompt_item is not None:
            try:
                self.viewer_panel.removeItem(self.prompt_item)
                self.prompt_item.destroyed
            except Exception as e:
                print(e)

        self.prompt_item = BU.get_graphics_item(pm)
        self.start_p = self.mapToScene(event.pos())

        if pm == BC.PromptType.BOX:
            self.prompt_item.setPos(self.start_p.x(), self.start_p.y())
        elif pm == BC.PromptType.DOODLE:
            try:

                self.prompt_item.addToGroup(BU.get_point_on_view(self.start_p, 'red', BC.RADIUS))
            except Exception as e:
                print(f'MousePressEvent: {e}')
        elif pm == BC.PromptType.CLICK:
            pass
        elif pm == BC.PromptType.MASK:
            pass

        self.record_flag = True

    def mouseReleaseEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        print(f'Released!')
        self.start_p = None

        if not self.record_flag:
            return
        self.record_flag = False

        if self.root.model_worker.is_work():
            # try:
            self.send_prompt2thread()
            # except Exception as e:
            #     print('send_prompt2thread()', e)

    #  TODO: Clear the try ... except ...
    def plot_dicom(self, ww, wl):
        self.remove_dicom()
        norm_image = BU.dicom_map2_rgb(self.root.dicom_image, ww, wl)
        slice, w, h = norm_image.shape

        try:
            qimg = QImage(norm_image[int(self.root.frame_idx)].data, w, h, w, QImage.Format.Format_Grayscale8)
            qimg = QPixmap.fromImage(qimg)
            self.image_item = QGraphicsPixmapItem(qimg)
            self.image_item.setPos(0, 0)
            self.viewer_panel.addItem(self.image_item)
            self.viewer_panel.setSceneRect(self.sceneRect())
        except Exception as e:
            print('At plot_dicom, ', e)
        print(len(self.viewer_panel.items()))

    def show_information_on_status_bar(self, event):
        pos = self.mapToScene(event.pos())
        results = BU.extract_info_from_event(event, self.root.dicom_file, self.root.frame_idx, pos)
        self.root.show_cursor_info(**results)

    def show_mask(self, emitData):
        self.viewer_panel.removeItem(self.mask_item)
        mask = emitData.mask()
        h, w = emitData['size']
        qimg = QImage(mask, w, h, w, QImage.Format.Format_RGB888)
        qimg = QPixmap.fromImage(qimg)
        self.mask_item = QGraphicsPixmapItem(qimg)
        self.mask_item.setPos(0, 0)
        self.mask_item.setOpacity(.5)
        self.viewer_panel.addItem(self.mask_item)
        self.viewer_panel.setSceneRect(self.sceneRect())



    def build_bbox_prompt(self, current_p: QPointF, image_shape=[512, 512]):
        self.remove_prompt()
        sx, sy = self.start_p.x(), self.start_p.y()
        cx, cy = current_p.x(), current_p.y()

        minx, maxx = [cx, sx][:: -1 if cx > sx else 1]
        miny, maxy = [cy, sy][:: -1 if cy > sy else 1]
        minx, miny = [max(n, 0) for n in [minx, miny]]
        maxx, maxy = min(maxx, image_shape[0]), min(maxy, image_shape[1])

        self.prompt_item = QGraphicsRectItem(QRectF(minx, miny, maxx - minx, maxy - miny))
        self.prompt_item.setPen(QPen(QColor('red')))
        self.viewer_panel.addItem(self.prompt_item)

    def build_doodle_prompt(self, current_p: QPointF):
        self.remove_prompt()
        self.prompt_item.addToGroup(BU.get_point_on_view(current_p, 'color', BC.RADIUS))
        self.viewer_panel.addItem(self.prompt_item)
        pass

    def build_click_prompt(self, event):
        pass

    def build_mask_prompt(self, event):
        pass

    def remove_prompt(self):
        self.viewer_panel.removeItem(self.prompt_item)

    def remove_dicom(self):
        self.viewer_panel.removeItem(self.image_item)

    def send_prompt2thread(self):
        boxes, labels, coords, masks, is_doodle = [None] * 5

        if self.root.prompt_mode == BC.PromptType.CLICK:
            coords = [[self.prompt_item.x(), self.prompt_item.y()]]
            labels = [[1]]
        if self.root.prompt_mode == BC.PromptType.BOX:
            rect = self.prompt_item.rect()
            boxes = [rect.topLeft().x(), rect.topLeft().y(), rect.bottomRight().x(), rect.bottomRight().y()]
            boxes = torch.as_tensor(boxes, dtype=torch.float).unsqueeze(0)
        if self.root.prompt_mode == BC.PromptType.DOODLE:
            pass
        if self.root.prompt_mode == BC.PromptType.MASK:
            pass

        self.root.model_worker.decode_mask({
            'points': (coords, labels),
            'boxes': boxes,
            'masks': masks
        })

