from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSlider, QGridLayout
from typing import Union

from napari.components import Dims


class QtDims(QWidget):

    _slider_height = 19

    update_axis = pyqtSignal(int)

    sliders = []

    def __init__(self, dims: Dims):
        super().__init__()

        self.dims = dims

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setFixedHeight(0)

        for axis in range(0,dims.nb_dimensions):
            self.get_or_create_slider(axis)


        self.update_axis.connect(self.update_slider)

        def update_dims(source, axis):
            self.update_axis.emit(axis)

        self.dims.add_listener(update_dims)

    @property
    def num_sliders(self):
        return len(self.sliders)

    def get_or_create_slider(self, axis):
        """Updates a slider for the given axis or creates
        it if it does not already exist.

        Parameters
        ----------
        axis : int
            Axis that this slider controls.

        Returns
        -------
        slider : PyQt5.QSlider or None
            Updated slider, if it exists.
        """

        grid = self.layout()

        while axis>=self.num_sliders:
            new_slider_axis = self.num_sliders
            slider = self.create_slider_widget()
            grid.addWidget(slider, new_slider_axis, 0)
            self.sliders.append(slider)

            slider.valueChanged.connect(lambda value: self.dims.set_point(new_slider_axis, value))

        #slider.setMaximum(max_axis_length - 1)

        self.setFixedHeight(self.num_sliders*self._slider_height)

        return slider


    def update_slider(self, axis: int):
        slider = self.sliders[axis]
        slider.setValue(self.dims.get_point(axis))



    def create_slider_widget(self):
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setMinimum(0)
        slider.setFixedHeight(17)
        slider.setTickPosition(QSlider.NoTicks)
        # slider.setTickPosition(QSlider.TicksBothSides)
        # tick_interval = int(max(8,max_axis_length/8))
        # slider.setTickInterval(tick_interval)
        slider.setSingleStep(1)
        return slider



    #
    # class QtDims(QWidget):
    #     SLIDERHEIGHT = 19
    #
    #     def __init__(self, dims):
    #         super().__init__()
    #
    #         dims.events.update_slider.connect(self.update_slider)
    #         self._slider_value_changed = dims._slider_value_changed
    #         self.sliders = []
    #
    #         layout = QGridLayout()
    #         layout.setContentsMargins(0, 0, 0, 0)
    #         self.setLayout(layout)
    #         self.setFixedHeight(0)
    #
    #     def _axis_to_row(self, axis, max_dims):
    #         message = f'axis {axis} out of bounds for {max_dims} dims'
    #
    #         if axis < 0:
    #             axis = max_dims - axis
    #             if axis < 0:
    #                 raise IndexError(message)
    #         elif axis >= max_dims:
    #             raise IndexError(message)
    #
    #         if axis < 2:
    #             raise ValueError('cannot convert y/x-axes to rows')
    #
    #         return axis - 2
    #
    #     def update_slider(self, event):
    #         """Updates a slider for the given axis or creates
    #         it if it does not already exist.
    #
    #         Parameters
    #         ----------
    #         axis : int
    #             Axis that this slider controls.
    #         max_axis_length : int
    #             Longest length for this axis. If 0, deletes the slider.
    #
    #         Returns
    #         -------
    #         slider : PyQt5.QSlider or None
    #             Updated slider, if it exists.
    #         """
    #         axis = event.dim
    #         max_axis_length = event.dim_len
    #         max_dims = event.max_dims
    #
    #         grid = self.layout()
    #         row = self._axis_to_row(axis, max_dims)
    #
    #         slider = grid.itemAt(row)
    #         if max_axis_length <= 0:
    #             # delete slider
    #             grid.takeAt(row)
    #             return
    #
    #         if slider is None:  # has not been created yet
    #             # create slider
    #             if axis < 0:
    #                 raise ValueError('cannot create a slider '
    #                                  f'at negative axis {axis}')
    #
    #             slider = QSlider(Qt.Horizontal)
    #             slider.setFocusPolicy(Qt.StrongFocus)
    #             slider.setMinimum(0)
    #             slider.setFixedHeight(17)
    #             slider.setTickPosition(QSlider.NoTicks)
    #             # slider.setTickPosition(QSlider.TicksBothSides)
    #             # tick_interval = int(max(8,max_axis_length/8))
    #             # slider.setTickInterval(tick_interval)
    #             slider.setSingleStep(1)
    #
    #             grid.addWidget(slider, row, 0)
    #             self.sliders.append(slider)
    #         else:
    #             slider = slider.widget()
    #
    #         slider.valueChanged.connect(lambda value:
    #                                     self._slider_value_changed(value, axis))
    #         slider.setMaximum(max_axis_length - 1)
    #         self.setFixedHeight((max_dims-2)*self.SLIDERHEIGHT)
    #         return slider

