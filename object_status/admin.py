from django.contrib import admin

from .models import IN_PROGRESS, IN_PRODUCTION, NEEDS_REVIEW

from .utils import StatusPermissions, StatusEmail


class StatusBaseView:
  def has_change_permission(self, request, obj=None):
    """Returns true if the current user has permission to change the requested object."""
    if obj:
      perms = StatusPermissions.from_model(self.model)
      if obj.status == IN_PROGRESS:
        return True # Anyone can edit an object in progress
      elif obj.status == NEEDS_REVIEW:
        return request.user.has_perm(perms.change_needs_review(full=True))
      elif obj.status == IN_PRODUCTION:
        return request.user.has_perm(perms.change_in_production(full=True))
    return super().has_change_permission(request)

class StatusBaseAdmin(StatusBaseView, admin.ModelAdmin):
  readonly_fields = ('status',)
  # change_form_template = 'admin/status/change_form.html'
  # change_list_template = 'admin/status/change_list.html'

  def change_view(self, request, object_id, form_url='', extra_context=None):
    """Passes extra data to change_form.html"""
    extra_context = extra_context or {}
    
    # Status info
    status = self.model.objects.get(pk=object_id).status
    extra_context['IN_PROGRESS'] = status == IN_PROGRESS
    extra_context['NEEDS_REVIEW'] = status == NEEDS_REVIEW
    extra_context['IN_PRODUCTION'] = status == IN_PRODUCTION

    # Permission info
    perms = StatusPermissions.from_model(self.model)
    extra_context['CAN_REJECT'] = request.user.has_perm(perms.reject_needs_review(full=True))
    extra_context['CAN_REMOVE'] = request.user.has_perm(perms.remove_from_production(full=True))
    extra_context['CAN_PUSH'] = request.user.has_perm(perms.push_to_production(full=True))
    return super().change_view(request, object_id, form_url, extra_context=extra_context)

  def add_view(self, request, form_url='', extra_context=None):
    extra_context = extra_context or {}
    extra_context['IN_PROGRESS'] = True
    return super().add_view(request, form_url, extra_context)

  def save_model(self, request, obj, form, change):
    """Changes the object's status depending on which button was
    clicked and saves the object to the database."""
    email = StatusEmail(obj)
    request_keys = request.POST.keys()
    if '_submitforreview' in request_keys:
      obj.status = NEEDS_REVIEW
      email.needs_review()
    elif '_pushtoproduction' in request_keys:
      obj.status = IN_PRODUCTION
    elif '_rejectfromreview' in request_keys:
      obj.status = IN_PROGRESS
    elif '_removefromproduction' in request_keys:
      obj.status = IN_PROGRESS
      email.remove_from_production()
    super().save_model(request, obj, form, change)

class StatusBaseInline(StatusBaseView, admin.TabularInline):
  def has_add_permission(self, request, obj=None):
    return self.has_change_permission(request, obj=obj)