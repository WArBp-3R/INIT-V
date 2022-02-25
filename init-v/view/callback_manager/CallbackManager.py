import dash
from dash.dependencies import Output, Input, State

from view import GUI_Handler


class Callback:
    def __call__(self, *args, **kwargs):
        trigger_ctx = CallbackManager.get_input_context()
        trigger_ctx_input = Input(trigger_ctx[0], trigger_ctx[1])
        if trigger_ctx_input not in self.register.keys():
            return self.default_outputs
        else:
            self.register[trigger_ctx_input]()

    def __init__(self,
                 output_list: list[Output]):
        self.output_list = output_list
        self.input_list: list[Input] = []
        self.state_list: list[State] = []
        self.register: dict[Input, any] = {}

        self.default_outputs = [None for o in self.output_list]

    def add_function(self, input: Input, state_list: list[State], function: any):
        self.register[input] = function
        # self.input_list =
        # self.state_list


class CallbackManager:
    def __init__(self, gui_handler: GUI_Handler):
        self.gui_handler = gui_handler
        self.callback_register: dict[list[Output], Callback] = {}

    @staticmethod
    def get_input_context():
        ctx = dash.callback_context
        return tuple(ctx.triggered[0]['prop_id'].split('.')) if ctx.triggered else (None, None)

    def register_callback(self,
                          output_list: list[Output],
                          input: Input,
                          state_list: list[State],
                          func: any):
        if output_list not in self.callback_register.keys():
            self.callback_register[output_list] = Callback(output_list)
        self.callback_register[output_list].add_function(input, state_list, func)

    def set_default_outputs(self, output_list: list[Output], default_outputs: list[any]):
        if output_list in self.callback_register.keys():
            self.callback_register[output_list].default_outputs = default_outputs

    def finalize_callbacks(self):
        pass
