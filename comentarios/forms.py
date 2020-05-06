from django.forms import ModelForm
from decouple import config
from .models import Comentario
import requests


class FormComentario(ModelForm):
    def clean(self):
        raw_data = self.data
        recaptcha_response = raw_data.get('g-recaptcha-response')

        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': config('RECAPTCHA_TOKEN_SERVER'),
                'response': recaptcha_response
            }
        )
        recaptcha_result = recaptcha_request.json()
        if not recaptcha_result.get('success'):
            self.add_error(
                'comentario',
                'reCAPTCHA inválido. Tente novamente.'
            )

        cleaned_data = self.cleaned_data
        nome = cleaned_data.get('nome_comentario')

        if len(nome) < 5:
            self.add_error(
                'nome_comentario',
                'Nome precisa ter mais de 5 caracteres.')

    class Meta:
        model = Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')
