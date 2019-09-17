from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


class Permissions:
  """This is the base class for all custom permissions. To create a new permission set, subclass
  this class."""
  def __init__(self, model_name, app_label):
    self.model_name = model_name.lower()
    self.app_label = app_label

  @classmethod
  def from_model(cls, model):
    return cls(model.__name__, model._meta.app_label)

  def _template(self, action, detail=None, full=False, codename_only=True):
    """This method defines a common permission template which all permissions use and
    should only be called by subclasses.
    
    Parameters:
      action (str): The action with which this permission is associated. Should be
                    all lower-case and snake-case.
      detail (str): Additional detail about how the action and model are related. Should be
                    all lower-case snake-case.
      full (bool): Whether the full permission name should be used (i.e. app name prepended)
      codename_only (bool): Whether just the codename should be returned
    
    Returns:
      str or (str, str): Either the codename or (codename, name), depending on the
                         codename_only parameter
    """
    model, prefix = self.model_name, f'{self.app_label}.' if full else ''
    detail = '_' + detail if detail else '' # Prepend '_' if detail was provided
    codename = f'{prefix}{action}_{model}{detail}'
    name = f'Can {action} {model}{" ".join(detail.split("_"))}'
    return codename if codename_only else (codename, name)

  def all(self, full=False, codename_only=False):
    """Gets a list of all permissions"""
    def is_permission(attr_name):
      """Returns true if attr_name refers to a permission method"""
      attr = getattr(self.__class__, attr_name)
      if callable(attr) and attr_name != 'all':
        # True if attr is 1) not private and 2) not a class method
        return not attr_name.startswith('_') and not hasattr(attr, '__self__')
      return False

    return [getattr(self, attr)(full, codename_only) for attr in dir(self.__class__) if is_permission(attr)]

class StatusPermissions(Permissions):
  """Permissions having to do with the status of an object."""
  def change_needs_review(self, full=False, codename_only=True):
    return self._template('change', 'needs_review', full=full, codename_only=codename_only)

  def change_in_production(self, full=False, codename_only=True):
    return self._template('change', 'in_production', full=full, codename_only=codename_only)
    
  def reject_needs_review(self, full=False, codename_only=True):
    return self._template('reject', 'needs_review', full=full, codename_only=codename_only)

  def remove_from_production(self, full=False, codename_only=True):
    return self._template('remove', 'from_production', full=full, codename_only=codename_only)
  
  def push_to_production(self, full=False, codename_only=True):
    return self._template('push', 'to_production', full=full, codename_only=codename_only)

class StatusEmail:
  def __init__(self, obj):
    self.obj = obj
    self.model_name = obj.__class__.__name__
    self.perms = StatusPermissions(self.model_name)

  def needs_review(self):
    perm = self.perms.change_needs_review(full=True)
    users = get_user_model().objects.all()
    recipients = [user.email for user in users if user.has_perm(perm)]
    send_mail(
      f'{self.model_name} needs review',
      f'The {self.model_name.lower()} {self.obj} is ready for review.',
      settings.STATUS_CHANGE_EMAIL_FROM,
      recipients
    )
  
  def remove_from_production(self):
    perm = self.perms.change_needs_review(full=True)
    users = get_user_model().objects.all()
    recipients = [user.email for user in users if not user.has_perm(perm)]
    send_mail(
      f'{self.model_name} removed from production',
      f'The {self.model_name.lower()} {self.obj} has a problem and has been removed from production.',
      settings.STATUS_CHANGE_EMAIL_FROM,
      recipients
    )
