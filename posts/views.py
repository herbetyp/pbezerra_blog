from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages
from django.views import View
from decouple import config
from .models import Post


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('categoria_post')
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )
        return qs


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()

        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo) |
            Q(publicado_post__icontains=termo) |
            Q(excerto_post__icontains=termo)
        )
        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs

        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs


class PostDetalhes(View):
    template_name = 'posts/post_detalhes.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk, publicado_post=True)
        self.contexto = {
            'post': post,
            'comentarios': Comentario.objects.filter(
                post_comentario=post, publicado_comentario=True,),
            'form': FormComentario(request.POST or None),
            'token_recaptcha': config('RECAPTCHA_TOKEN_CLIENT')
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)

    def post(self, request, *args, **kwargs):
        form = self.contexto['form']

        if not form.is_valid():
            return render(request, self.template_name, self.contexto)

        comentario = form.save(commit=False)

        if request.user.is_authenticated:
            comentario.usuario_comentario = request.user

        comentario.post_comentario = self.contexto['post']
        comentario.save()
        messages.success(request, 'Seu comentário foi enviado para revisão.')

        return redirect('post_detalhes', pk=self.kwargs.get('pk'))
