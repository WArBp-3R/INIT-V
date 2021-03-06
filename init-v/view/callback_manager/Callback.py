import dash
import logging
from dash.dependencies import Output, Input, State


class Callback:
    def __call__(self, *args, **kwargs):
        trigger_ctx = self.get_input_context()
        trigger_ctx_input = Input(trigger_ctx[0], trigger_ctx[1])

        output = None
        if trigger_ctx_input in self.register.keys():
            output = self.register[trigger_ctx_input](
                args[self.input_list.index(trigger_ctx_input)],
                *[args[len(self.input_list) + x] for x in self.input_state_indexes[trigger_ctx_input]])

        if output:
            for i in range(0, len(output)):
                output[i] = output[i] if output[i] else self.default_outputs[i]
        else:
            output = self.default_outputs

        log_msg = "Callback for {} triggered by {}"
        logging.debug(log_msg.format(self.output_list, trigger_ctx_input))

        return output

    def __init__(self,
                 output_list: list[Output]):
        self.output_list = output_list
        self.input_list: list[Input] = []
        self.state_list: list[State] = []
        self.register: dict[Input, any] = {}
        self.input_state_indexes: dict[Input, list[int]] = {}

        self.default_outputs: list[any] = [None for o in self.output_list]

    @staticmethod
    def get_input_context():
        ctx = dash.callback_context
        return tuple(ctx.triggered[0]['prop_id'].split('.')) if ctx.triggered else (None, None)

    def add_function(self, func: any, input: Input, state_list: list[State] = None):
        if not state_list:
            state_list = []

        if input not in self.register.keys():
            self.input_list.append(input)

        s_idx_list = []  # add states
        for s in state_list:
            if s in self.state_list:
                s_idx_list.append(self.state_list.index(s))
            else:
                s_idx_list.append(len(self.state_list))
                self.state_list.append(s)

        self.register[input] = func
        self.input_state_indexes[input] = s_idx_list
