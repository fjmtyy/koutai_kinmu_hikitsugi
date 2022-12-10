from .models import Handover, Comment, HandoverImage
from .forms import PostForm, ImageForm, CommentForm, SearchForm
from django.views.generic import CreateView, ListView, FormView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime
from django.core.exceptions import ValidationError


class HandoverPostView(CreateView):
    """
    引継ぎを投稿VIEW
    """
    template_name = 'handover/post.html'
    model = Handover
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageForm
        return context

    def form_valid(self, form):
        if self.request.method == 'POST':
            try:
                self.check_extension()
            except ValidationError:
                form.add_error(None, '拡張子を確認してください')
            else:
                self.post_handover_data()
                return HttpResponseRedirect(self.get_success_url())
            return render(self.request, self.template_name, {'form': form, 'image_form': ImageForm})

    def check_extension(self):
        """
        拡張子を確認する
        :return:
        """
        image = self.request.FILES.getlist('image')
        extension = (
            '.png',
            '.jpeg',
            '.jpg',
            '.gif',
            '.tif',
            '.tiff',
            '.bmp'
        )
        for image in image:
            if not image.name.endswith(extension):
                raise ValidationError('拡張子を確認してください')

    def post_handover_data(self):
        """
        DBに保存するための情報の生成と保存を行う
        :return:
        """
        # 入力された引継ぎ情報を生成している
        # 引継ぎに画像があるか否かで生成する情報を分けている
        handover_post_data = Handover(
            handover=self.request.POST['handover'],
            user_ID=self.request.user.user_ID,
            user_name=self.request.user.get_full_name(),
            created_at=timezone.now()
        )
        # 保存
        handover_post_data.save()

        # imageがあった場合にHandoverImageに保存処理
        image_data = self.request.FILES.getlist('image')
        if image_data is not None:
            handover_no = handover_post_data.handover_no
            queryset = Handover.objects.get(pk=handover_no)
            for post_image in image_data:
                image_post_data = HandoverImage(
                    handover_id=queryset.handover_no,
                    image=post_image,
                )
                image_post_data.save()

        # HandoverTagRelation tag 保存処理
        tag_data = self.request.POST.getlist("tag")
        for post_tag in tag_data:
            handover_post_data.tag.add(post_tag)

    def get_success_url(self):
        """
        投稿機能が成功した場合の遷移先
        :return:
        """
        return reverse_lazy('handover:top')


class HandoverListView(HandoverPostView, ListView):
    """
    TOPから引継ぎを投稿する　HandoverPostViewを継承
    TOPに引継ぎを表示する　listviewをオーバライド
    """
    template_name = 'handover/top.html'
    model = Handover
    form_class = PostForm
    paginate_by = 10

    def __init__(self):
        super().__init__()
        self.search_ID = None
        self.search_date = None
        self.tag_data = []
        self.contributor_ID = Q()
        self.date = Q()
        self.tag = Q()

    def get_context_data(self, **kwargs):
        context = super(HandoverListView, self).get_context_data(**kwargs)
        context.update(dict(get_method_string=self.request.GET.urlencode()))
        return context

    def get_search_data(self):
        """
        検索情報をGETするための関数
        :return:
        """
        self.search_ID = self.request.GET.get('search_contributor_ID')
        self.search_date = self.request.GET.get('search_date')
        # タグに関しては、検索かタグボタンを押して検索できるので処理を分けている
        if 'search_tag' in self.request.GET:
            self.tag_data = self.request.GET.getlist('search_tag')
        if 'push_tag' in self.request.GET:
            self.tag_data = self.request.GET.getlist('push_tag')

    def get_queryset_data(self):
        """
        検索された情報をGETしてインスタンス化する
        :return:
        """
        if self.search_ID is not None and self.search_ID != '':
            self.contributor_ID = Q(user_ID=self.search_ID)
        if self.search_date is not None and self.search_date != '':
            date_data = self.search_date.split('～')
            date_start = date_data[0]
            date_end = date_data[1]
            self.date = Q(created_at__range=(date_start, date_end))
        if self.tag_data:
            self.tag = Q(tag__in=self.tag_data)

    def get_queryset(self):
        """
        インスタンス化された情報を基にqueryを生成している
        検索情報がなければ直近1日のデータを表示する
        :return:
        """
        self.get_search_data()
        if self.search_ID is not None or self.search_date is not None or self.tag_data:
            self.get_queryset_data()
            queryset = self.model.objects.annotate(
                Count('comment')
            ).filter(
                self.contributor_ID |
                self.date |
                self.tag
            ).order_by('-handover_no')
        else:
            queryset = self.model.objects.annotate(
                Count('comment')
            ).all(
            ).order_by("-handover_no")
        return queryset


class CommentPostView(CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        """
        引継ぎに対するreply
        コメントに対するreply
        処理を分けている
        :return:
        """
        if self.request.method == 'POST':
            if 'handover_reply' in self.request.POST:
                self.handover_reply_data()
            elif 'comment_reply' in self.request.POST:
                self.comment_reply_data()
            return HttpResponseRedirect(
                reverse_lazy(
                    'handover:handover_detail',
                    kwargs={'pk': self.kwargs['pk']}
                )
            )

    def handover_reply_data(self):
        """
        引継ぎに対するreplyのdataを生成している
        parent_idがNoneなのでcommentに紐づけない
        :return:
        """
        queryset = Handover.objects.get(pk=self.kwargs['pk'])
        comment_data = Comment(
            comments=self.request.POST['comments'],
            handover_id=queryset.handover_no,
            parent_id=None,
            User_ID=self.request.user.user_ID,
            user_name=self.request.user.get_full_name(),
            created_at=timezone.now()
        )
        # 保存
        comment_data.save()

    def comment_reply_data(self):
        """
        引継ぎに対するreplyのdataを生成している
        parent_idをreplyしたcommentに紐づけている
        :return:
        """
        queryset = Handover.objects.get(pk=self.kwargs['pk'])
        comment_data = Comment(
            comments=self.request.POST['comments'],
            handover_id=queryset.handover_no,
            parent_id=self.request.POST['comment_reply'],
            User_ID=self.request.user.user_ID,
            user_name=self.request.user.get_full_name(),
            created_at=datetime.now()
        )
        # 保存
        comment_data.save()


class HandoverDetailView(CommentPostView, DetailView):
    """
    各引継ぎにあるコメントを表示する DetailView
    引継ぎへのcommentやそれに対するreplyなどを投稿する CommentPostView
    """
    model = Handover
    template_name = 'handover/detail.html'

    def get_context_data(self, **kwargs):
        """
        comment_list　引継ぎへコメントしたものを絞り込むqueryset
        reply_form　コメントを投稿するform
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['comment_list'] = self.object.comment_set.filter(
            parent__isnull=True
        )
        context['reply_form'] = CommentForm
        return context
    

class HandoverSearchView(FormView):
    form_class = SearchForm
    template_name = 'handover/search.html'

    def form_valid(self, form):
        """
        formの入力情報をGETでHandoverListViewに受け渡している
        """
        if self.request.method == 'GET':
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        検索情報に問題なかった場合の遷移先
        :return:
        """
        return reverse_lazy('handover:top')
    