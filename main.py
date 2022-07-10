
__author__="Caio"
__date__ ="$07/07/2019 15:10:02$"

# importando bibliotecas método por método, para evitar erro de chamado
import kivy
from kivy.lang.builder import Builder
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.metrics import dp, sp

# Funções matemáticas
from math import *

# Importando biblioteca sys
import sys

# Predefinir tamanho inicial do display
from kivy.config import Config

# Tamanho minimo
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '580')

# Tamanho inicial
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '580')

# KivyMD (Deixando a interface mais moderna)
import kivymd
from kivymd.app import App
from kivymd.app import MDApp
from kivymd.theming import App
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog

# Alterar fonte-padrão
from kivy.core.text import LabelBase

# Executar kivy sem OpenGL
from kivy import Config
Config.set('graphics', 'multisamples', '0')

class Gerenciador(ScreenManager):
    pass

# Funções do menu
class Menu(Screen):

    # Popup Créditos
    def creditos_popup(self):
        creditos = BoxLayout(orientation='vertical')
        creditos.add_widget(Label(text="AMENPREV"))
        creditos.add_widget(Label(text="(Aplicativo de Mensuração e Previsão de Volatilidade)"))
        creditos.add_widget(Label(text="Desenvolvimento: Caio Cardoso da Cunha"))
        creditos.add_widget(Label(text="2019"))
        popup = Popup(title="Sobre", content=creditos, size_hint=(None, None), size=(500, 300))
        popup.open()


# Cálculo da pressão de vapor da mistura, baseado nos coeficientes de Antoine
class Pressvap(Screen):

    a = ObjectProperty(None)
    b = ObjectProperty(None)
    unipress = ObjectProperty(None)
    resultado = ObjectProperty(None)
    unidade = ObjectProperty(None)

    ind_press_parcial = []

    def save(self):
        if len(self.a.text and self.b.text and self.unipress.text) > 0:
            fracmol = float(self.a.text)
            pp = float(self.b.text)
            mult = pp * fracmol
            self.ind_press_parcial.append(mult)

        else:
            self.resultado.text = "Adicione os dados primeiro"

    def calcpress(self):
        if len(self.ind_press_parcial) > 0:
            up = self.unipress.text
            v = sum(self.ind_press_parcial)
            self.resultado.text = str(v)
            self.unidade.text = up
            self.ind_press_parcial.clear()
        else:
            pass

    def limpar(self):
        self.ind_press_parcial.clear()

# Comparar percentualmente pressão de vapor entre substâncias
class Classtemp(Screen):

    c = ObjectProperty(None)
    d = ObjectProperty(None)
    e = ObjectProperty(None)
    f = ObjectProperty(None)
    classificar1 = ObjectProperty(None)
    classificar2 = ObjectProperty(None)

    def comparador(self):

        if len(self.c.text and self.d.text and self.e.text and self.f.text) > 0:
            subs1 = str(self.c.text)
            subs2 = str(self.e.text)
            press1 = float(self.d.text)
            press2 = float(self.f.text)

            if press1 > press2:
                comp1 = abs(round((((press1/press2)-1)*100), 2))
                comp2 = abs(round((((press2/press1)-1)*100), 2))

                resultado1 = subs1 + " é " + str(comp1) + " % mais volátil que " + subs2
                resultado2 = subs2 + " é " + str(comp2) + " % menos volátil que " + subs1
                self.classificar1.text = resultado1
                self.classificar2.text = resultado2

            else:
                self.classificar1.text = "Coloque o maior valor acima"

        else:
            self.classificar1.text = "Digite todos os valores"

# LabelBase é o banco de tipografias
LabelBase.register(name="Cordia", fn_regular="CORDIA.ttf")

# Aplicativo (interface inicial e chamada de programa)
class Amenprev(MDApp):

# Cores para configurar KivyMD 
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Green'
    theme_cls.primary_palette = 'Blue'
    theme_cls.theme_style = 'Dark'

# Animação Inicial
    def animation(self, widget, *args):
        anim = Animation(opacity=0, duration=0.4)
        anim += Animation(top=1, duration=0.3)
        anim.start(widget)

    def build(self):
        # Variável armazena caminho da pasta onde se encontram os arquivos
        current_path = sys.path[0]

        # Caminho da interface
        interface = open(current_path + "/interface.kv")

        # Chamando arquivo .kv para execução
        Builder.load_string(interface.read(), encoding="utf-8", rulesonly=True)
                                            # Comando que interpreta acentuações do português (utf-8)

        # Chamando função do menu
        return Gerenciador()

Amenprev().run()

