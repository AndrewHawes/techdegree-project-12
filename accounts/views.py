from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView

from .forms import CustomUserCreationForm, ProfileEditForm, ProfileSkillFormSet
from .models import Profile
from .tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Team Builder Account'
            message = render_to_string(
                'accounts/emails/account_activation_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                }
            )
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)

        messages.success(request, 'Your account has been activated!')
        return redirect('profile_edit')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = Profile

    def get_object(self, queryset=None):
        if not self.kwargs.get('pk'):  # accessing logged in user's profile
            profile = (
                Profile.objects
                .select_related('user')
                .prefetch_related('user__owned_projects')
                .prefetch_related('user__positions__project')
                .prefetch_related('user__applications__position__project')
                .prefetch_related('skills')
                .get(user=self.request.user)
            )
            return profile

        return super().get_object()

    def get_queryset(self):
        queryset = (
            Profile.objects
            .select_related('user')
            .prefetch_related('user__owned_projects')
            .prefetch_related('user__positions__project')
            .prefetch_related('skills')
        )
        return queryset


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['formset'] = ProfileSkillFormSet(self.request.POST, profile=self.object)
        else:
            data['formset'] = ProfileSkillFormSet(profile=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            profile = form.save()
            for subform in formset:
                skill = subform.save()
                if skill:
                    if subform.cleaned_data.get('DELETE'):
                        profile.skills.remove(skill)
                    else:
                        profile.skills.add(skill)
            profile.save()
        else:
            return self.render_to_response(context)
        return super().form_valid(form)

    def get_object(self, *args, **kwargs):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile')
