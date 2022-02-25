import dash
from dash.dependencies import Output, Input, State

from view import GUI_Handler
from view.callback_manager.Callback import Callback


class CallbackManager:
    def __init__(self, gui_handler: GUI_Handler):
        self.gui_handler = gui_handler
        self.callback_register: dict[tuple[Output], Callback] = {}

    def register_callback(self,
                          func: any,
                          output_list: list[Output],
                          input: Input,
                          state_list: list[State] = None,
                          default_outputs: list[any] = None):
        output_tuple = tuple(output_list)
        if output_tuple not in self.callback_register.keys():
            self.callback_register[output_tuple] = Callback(output_list)
        self.callback_register[output_tuple].add_function(func, input, state_list)
        if default_outputs:
            self.set_default_outputs(output_list, default_outputs)

    def register_multiple_callbacks(self,
                                    output_list: list[Output],
                                    func_state_register: dict[Input, tuple[any, State]],
                                    default_outputs: list[any] = None):
        for k, v in func_state_register.items():
            self.register_callback(v[0], output_list, k, v[1])
        if default_outputs:
            self.set_default_outputs(output_list, default_outputs)

    def set_default_outputs(self, output_list: list[Output], default_outputs: list[any]):
        output_tuple = tuple(output_list)
        if output_tuple not in self.callback_register.keys():
            self.callback_register[output_tuple] = Callback(output_list)
        self.callback_register[output_tuple].default_outputs = default_outputs

    def finalize_callbacks(self):
        for v in self.callback_register.values():
            self.gui_handler.app.callback(
                v.output_list,
                v.input_list,
                v.state_list
            )(v)
