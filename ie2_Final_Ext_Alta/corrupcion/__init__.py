from pickle import NONE
from tkinter import Widget
from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = ('corrupcion')
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 5
    dotacion = 50
    Ciudadano1_ROLE = 'Ciudadano1'
    Ciudadano2_ROLE = 'Ciudadano2'
    Oficial_ROLE = 'Oficial'
    Monitor_ROLE = 'Monitor'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    gato = models.BooleanField(initial=False)
    soborno_aceptado = models.BooleanField(initial=False)


class Player(BasePlayer):
    hola_ciudadano = models.BooleanField(
        initial = False,
        choices=[
            [True, 'Ofrecer soborno'],
            [False, 'No ofrecer soborno']
        ]
    )

    pokis_oficial = models.BooleanField(
        initial = False,
        choices=[
            [True, 'Aceptar soborno'],
            [False, 'No aceptar soborno']
        ]
    )

    p1 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p2 = models.BooleanField(
        choices=[
            [False, 'Verdadero'],
            [True, 'Solo al ciudadano 2']
        ]
    )

    p3 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p4 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p5 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p6 = models.BooleanField(
        choices=[
            [True, 'Verdadero'],
            [False, 'Falso']
        ]
    )

    p7 = models.LongStringField(

    )

    p8 = models.BooleanField(
        choices=[
            [True, 'Femenino'],
            [False, 'Masculino']
        ]
    )

    p9 = models.LongStringField(

    )

    p10 = models.LongStringField(

    )

    p11 = models.LongStringField(

    )
    p12 = models.BooleanField(
        choices=[
            [True, 'Derecha'],
            [False, 'Izquierda']
        ]
    )
    p13 = models.BooleanField(
        choices=[
            [True, 'Opción 1'],
            [False, 'Opción 2']
        ]
    )

    p14 = models.BooleanField(
        choices=[
            [True, 'Opción 1'],
            [False, 'Opción 2']
        ]
    )

    p15 = models.BooleanField(
        choices=[
            [True, 'Opción 1'],
            [False, 'Opción 2']
        ]
    )

    p16 = models.BooleanField(
        choices=[
            [True, 'Opción 1'],
            [False, 'Opción 2']
        ]
    )

    monto_ciudadano_sinSoborno = models.IntegerField(min=1, max=10, blank=True)

    ambos_monto_ciudadano_conSoborno = models.IntegerField(Choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                           blank=True)  # agregue choices, no sirve para nada
    ambos_monto_oficial_conSoborno = models.IntegerField(Choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], blank=True)

    monto_ciudadano_conSoborno = models.IntegerField(min=1, max=10, blank=True)

    monto_oficial_conSoborno = models.IntegerField(min=1, max=10, blank=True)


# PAGES
class Instrucciones(Page):
    pass

    def is_displayed(self):
        # La página se mostrará si la ronda actual es menor o igual a 2
        return self.round_number <= 1


class Instrucciones_roles(Page):
    pass

    def is_displayed(self):
        # La página se mostrará si la ronda actual es menor o igual a 2
        return self.round_number <= 1


class Preguntas_control(Page):
    form_model = 'player'
    form_fields = ['p7']

    # 5 variables.
    # 2 tipos de pregunta
    def is_displayed(self):
        # La página se mostrará si la ronda actual es menor o igual a 2
        return self.round_number <= 1


class WaitPage_Ciudadano1(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano1' 


class WaitPage_Ciudadano2(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano2' 


class WaitPage_Oficial(WaitPage):

    @staticmethod
    def is_displayed(player):
        return player.role == 'Oficial' 


class WaitPage_Monitor(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.role == 'Monitor' 


class Ciudadano1(Page):
    form_model = 'player'
    form_fields = ['hola_ciudadano']

    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano1'


class WaitPageSoborno(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.hola_ciudadano  == False
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            if p.id_in_group == 1:
                group.gato = p.hola_ciudadano


class Oficial(Page):

    form_model = 'player'
    form_fields = ['pokis_oficial']

    @staticmethod
    def is_displayed(player):
        return player.group.gato and player.role == 'Oficial'


class WaitPageAceptarSoborno(WaitPage):
    
    @staticmethod
    def is_displayed(player):
        return player.hola_ciudadano  == False
    
    def is_displayed(player):
        group = player.group
        return group.gato

    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            if p.id_in_group == 3:
                group.soborno_aceptado = p.pokis_oficial
                # ACA NO HAY NADA DE SI NO SOBORNA


class MonitorsinSoborno(Page):
    form_model = 'player'
    form_fields = ['monto_ciudadano_sinSoborno']

    @staticmethod
    def is_displayed(player):
        group = player.group
        return (not player.group.soborno_aceptado) and player.role == 'Monitor' and group.gato 


class MonitorconSoborno(Page):
    
    
    form_model = 'player'
    form_fields = ['ambos_monto_ciudadano_conSoborno', 'ambos_monto_oficial_conSoborno', 'monto_oficial_conSoborno',
                   'monto_ciudadano_conSoborno',

                   ]

    @staticmethod
    def is_displayed(player):
        group = player.group
        return player.group.soborno_aceptado and player.role == 'Monitor' and group.gato    
    

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(group: Group):
        pass


class Resultados(Page):
    pass

class Final(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number >= 5

    pass

# FALTA CLASE CUANDO CIUDADANO NO SOBORNA

page_sequence = [#Instrucciones,
                 #Instrucciones_roles,
                 Preguntas_control,
                 WaitPage_Ciudadano2,
                 WaitPage_Oficial,
                 WaitPage_Monitor,
                 Ciudadano1,
                 # ResultadosSinSoborno,
                 WaitPageSoborno,
                 WaitPage_Ciudadano1,
                 WaitPage_Ciudadano2,
                 WaitPage_Monitor,
                 Oficial,
                 WaitPageAceptarSoborno,
                 WaitPage_Ciudadano1,
                 WaitPage_Ciudadano2,
                 WaitPage_Oficial,
                 MonitorsinSoborno,
                 MonitorconSoborno,
                 ResultsWaitPage,
                 Resultados,
                 Final]
