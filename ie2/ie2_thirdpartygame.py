
from otree.api import models, BasePlayer, BaseGroup, BaseSubsession, Currency
import random

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    dotacion_inicial = models.CurrencyField(min=0, initial=10)
    soborno_ofrecido = models.BooleanField(initial=False)
    soborno_aceptado = models.BooleanField(initial=False)
    castigo_realizado = models.BooleanField(initial=False)
    castigo_seleccionado = models.IntegerField(
        choices=list(range(1, 11)),  # Lista de valores del 1 al 10
        blank=True,
        widget=models.RadioSelect,
        label="Selecciona el nivel de castigo (1-10):"
    )

    def role(self):
        if self.id_in_group == 1:
            return 'Ciudadano 1'
        elif self.id_in_group == 2:
            return 'Oficial'
        elif self.id_in_group == 3:
            return 'Ciudadano 2'
        elif self.id_in_group == 4:
            return 'Monitor'

    def set_payoff(self):
        if self.role() == 'Ciudadano 1':
            self.payoff = self.dotacion_inicial - self.soborno_ofrecido * 3
        elif self.role() == 'Ciudadano 2':
            self.payoff = self.dotacion_inicial

    def set_soborno_aceptado(self):
        if self.role() == 'Oficial':
            self.soborno_aceptado = random.choice([True, False])

def set_castigo_realizado(self):
    if self.role() == 'Monitor':
        self.castigo_realizado = True
        if self.soborno_ofrecido and self.soborno_aceptado:
            # Escenario b: castigar ciudadano y/o oficial
            if self.castigo_seleccionado == 1:
                self.payoff = -self.castigo_seleccionado
            elif self.castigo_seleccionado == 2:
                self.payoff = -self.castigo_seleccionado
            elif self.castigo_seleccionado == 3:
                self.payoff = -self.castigo_seleccionado

        elif self.soborno_ofrecido and not self.soborno_aceptado:
            # Escenario a: castigar ciudadano
            if self.castigo_seleccionado == 1:
                self.payoff = -self.castigo_seleccionado

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class OfrecerSoborno(Page):
    form_model = 'player'
    form_fields = ['soborno_ofrecido']

class AceptarSoborno(Page):
    form_model = 'player'
    form_fields = ['soborno_aceptado']

    def before_next_page(self):
        self.player.set_soborno_aceptado()

class RealizarCastigo(Page):
    form_model = 'player'
    form_fields = ['castigo_seleccionado']

    def before_next_page(self):
        self.player.set_castigo_realizado()


class Results(Page):
    def vars_for_template(self):
        return {
            'soborno_ofrecido': self.player.soborno_ofrecido,
            'soborno_aceptado': self.player.soborno_aceptado,
            'castigo_realizado': self.player.castigo_realizado,
            'castigo_seleccionado': self.player.castigo_seleccionado,
            'payoff': self.player.payoff,
        }

page_sequence = [OfrecerSoborno, AceptarSoborno, RealizarCastigo, Results]

otree devserver