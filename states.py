from logging import error
from transitions import Machine, State

class Order():
    def __init__(self) -> None:
        self.order_pizza_size = None
        self.order_pay_type = None


class Ordering(Order):
    states = [
        State(name='start'),

        State(name='pizza_size', on_enter='pizza_size_state'),
        State(name='pay_type', on_enter='pay_type_state'),
        State(name='confirm', on_enter='confirm_state'),
        
        State(name='end', on_enter='end_state')
    ]

    transitions = [
        {'trigger': 'start', 'source': 'start', 'dest': 'pizza_size'},

        {'trigger': 'big_pizza_chosen', 'source': 'pizza_size', 'dest': 'pay_type'},
        {'trigger': 'small_pizza_chosen', 'source': 'pizza_size', 'dest': 'pay_type'},

        {'trigger': 'cash_type_chosen', 'source': 'pay_type', 'dest': 'confirm'},
        {'trigger': 'card_type_chosen', 'source': 'pay_type', 'dest': 'confirm'},

        {'trigger': 'confirmed', 'source': 'confirm', 'dest': 'end'},
        {'trigger': 'not_confirmed', 'source': 'confirm', 'dest': 'pizza_size'},
    ]


    def __init__(self, send_message, chat_id) -> None:
        super().__init__()
        self.send_message = send_message
        self.chat_id = chat_id
        self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial='start')

        self.transitions_ = (
            (self.states[1], ('большая', 'большой', 'большую', 'большою'), self.big_pizza_chosen_),
            (self.states[1], ('маленькая', 'маленькой', 'маленькую', 'маленькою'), self.small_pizza_chosen_), 
            
            (self.states[2], ('наличкой', 'нал'), self.cash_type_chosen_),
            (self.states[2], ('картой', ), self.card_type_chosen_), 
            
            (self.states[3], ('да', 'верно'), self.confirmed_),
            (self.states[3], ('нет', ), self.not_confirmed_)
        )

        self.error_counter = 0

    def start(self):
        self.machine.set_state('start')
        self.trigger('start')

    def get_message(self, msg: str):
        if self.state == self.states[0].name:
            self.send_message(self.chat_id, f'Напишите /order для оформления заказа')
            return
        for row in self.transitions_:
            if row[0].name == self.state and msg.lower() in row[1]:
                row[2]()
                break
        else:
            self.send_message(self.chat_id, f'Некорректный ответ [{self.error_counter + 1} try]')
            self.error_counter += 1
            if self.error_counter > 2:
                self.send_message(self.chat_id, f'Слишком много неправильных ответов!')
                self.machine.set_state('start')
                self.error_counter = 0


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def pizza_size_state(self):
        text = 'Какую вы хотите пиццу? Большую или маленькую?'
        self.send_message(self.chat_id, text)


    def pay_type_state(self):
        text = 'Как вы будете платить?'
        self.send_message(self.chat_id, text)

    def confirm_state(self):
        text = f'Вы хотите {self.order_pizza_size} пиццу, оплата - {self.order_pay_type}?'
        self.send_message(self.chat_id, text)

    def end_state(self):
        text = 'Спасибо за заказ'
        self.send_message(self.chat_id, text)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def big_pizza_chosen_(self):
        text = 'Вы выбрали большую пиццу'
        self.order_pizza_size = 'большую'
        self.send_message(self.chat_id, text)
        self.trigger('big_pizza_chosen')

    def small_pizza_chosen_(self):
        text = 'Вы выбрали маленькую пиццу'
        self.order_pizza_size = 'маленькую'
        self.send_message(self.chat_id, text)
        self.trigger('small_pizza_chosen')

    def cash_type_chosen_(self):
        self.order_pay_type = 'наличкой'
        self.trigger('cash_type_chosen')

    def card_type_chosen_(self):
        self.order_pay_type = 'картой'
        self.trigger('card_type_chosen')

    def confirmed_(self):
        self.trigger('confirmed')

    def not_confirmed_(self):
        self.trigger('not_confirmed')


